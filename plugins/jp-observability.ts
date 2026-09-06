import type { Plugin } from "@opencode-ai/plugin"
import { appendFile, mkdir } from "node:fs/promises"
import { homedir } from "node:os"
import { join } from "node:path"

const STATE_DIR = join(homedir(), ".local", "state", "jp-opencode")
const LOG_DIR = join(STATE_DIR, "logs")

const EVENT_LOG = join(LOG_DIR, "events.jsonl")
const TOOL_LOG = join(LOG_DIR, "tools.jsonl")
const ROUTING_LOG = join(LOG_DIR, "routing.jsonl")

type JsonRecord = Record<string, unknown>

type AssistantInfo = {
  id?: string
  sessionID?: string
  role?: string
  mode?: string
  agent?: string
  providerID?: string
  modelID?: string
  cost?: number
  finish?: string
  error?: unknown
  time?: {
    created?: number
    completed?: number
  }
  tokens?: {
    input?: number
    output?: number
    reasoning?: number
    cache?: {
      read?: number
      write?: number
    }
  }
}

const completedMessages = new Set<string>()
const escalatedMessages = new Set<string>()

const startedTools = new Map<string, number>()

const sessionParents = new Map<string, string>()
const sessionAgents = new Map<string, string>()

type PendingEscalation = {
  fromAgent: string
  fromSession: string
  timestamp: number
}

const pendingEscalations = new Map<string, PendingEscalation>()

async function writeJsonLine(path: string, data: JsonRecord) {
  try {
    await mkdir(LOG_DIR, { recursive: true })

    await appendFile(
      path,
      `${JSON.stringify({
        timestamp: new Date().toISOString(),
        ...data,
      })}\n`,
      "utf8",
    )
  } catch {
    // Observability must never break OpenCode.
  }
}

function stringValue(value: unknown): string | undefined {
  return typeof value === "string" && value.length > 0
    ? value
    : undefined
}

function numberValue(value: unknown): number {
  return typeof value === "number" && Number.isFinite(value)
    ? value
    : 0
}

function objectValue(value: unknown): Record<string, unknown> | undefined {
  if (!value || typeof value !== "object") {
    return undefined
  }

  return value as Record<string, unknown>
}

function classifyTier(agent: string): string {
  if (agent.endsWith("-lite")) {
    return "lite"
  }

  if (agent.endsWith("-heavy")) {
    return "heavy"
  }

  if (
    agent === "jp-code-orchestrator" ||
    agent === "jp-data-orchestrator"
  ) {
    return "orchestrator"
  }

  return "full"
}

function classifyFamily(agent: string): string {
  if (
    agent === "jp-data-orchestrator" ||
    agent.startsWith("jp-data-") ||
    agent.startsWith("jp-sql")
  ) {
    return "data"
  }

  return "code"
}

function isJPAgent(agent: string): boolean {
  return agent.startsWith("jp-")
}

function getAgent(info: AssistantInfo): string {
  return (
    stringValue(info.agent) ??
    stringValue(info.mode) ??
    "unknown"
  )
}

function getParentSession(sessionID: string): string | undefined {
  return sessionParents.get(sessionID)
}

function getDurationMs(info: AssistantInfo): number | undefined {
  const created = info.time?.created
  const completed = info.time?.completed

  if (
    typeof created !== "number" ||
    typeof completed !== "number"
  ) {
    return undefined
  }

  return Math.max(0, completed - created)
}

function isAssistantComplete(info: AssistantInfo): boolean {
  if (info.role !== "assistant") {
    return false
  }

  return (
    typeof info.time?.completed === "number" ||
    typeof info.finish === "string" ||
    info.error !== undefined
  )
}

function getSessionInfo(event: unknown): Record<string, unknown> | undefined {
  const root = objectValue(event)
  const properties = objectValue(root?.properties)

  return objectValue(properties?.info)
}

function getEventProperties(
  event: unknown,
): Record<string, unknown> | undefined {
  const root = objectValue(event)
  return objectValue(root?.properties)
}

function extractTaskAgent(args: unknown): string | undefined {
  const record = objectValue(args)

  return (
    stringValue(record?.subagent_type) ??
    stringValue(record?.agent)
  )
}

export const JPObservability: Plugin = async ({
  directory,
  worktree,
}) => {
  await writeJsonLine(EVENT_LOG, {
    event: "plugin.initialized",
    directory,
    worktree,
  })

  return {
    event: async ({ event }) => {
      /*
       * Session metadata
       */
      if (
        event.type === "session.created" ||
        event.type === "session.updated"
      ) {
        const info = getSessionInfo(event)

        const sessionID = stringValue(info?.id)
        const parentID = stringValue(info?.parentID)
        const agent = stringValue(info?.agent)

        if (sessionID && parentID) {
          sessionParents.set(sessionID, parentID)
        }

        if (sessionID && agent) {
          sessionAgents.set(sessionID, agent)
        }

        if (event.type === "session.created") {
          await writeJsonLine(EVENT_LOG, {
            event: "session.created",
            session_id: sessionID,
            parent_session_id: parentID,
            agent,
            directory,
          })
        }

        return
      }

      if (
        event.type === "session.compacted" ||
        event.type === "session.deleted" ||
        event.type === "session.error" ||
        event.type === "session.idle" ||
        event.type === "session.status"
      ) {
        const properties = getEventProperties(event)

        await writeJsonLine(EVENT_LOG, {
          event: event.type,
          session_id:
            stringValue(properties?.sessionID) ??
            stringValue(properties?.id),
          directory,
        })

        return
      }

      /*
       * Assistant generations
       *
       * OpenCode emits message.updated multiple times while a message
       * changes. We persist only the completed assistant message once.
       */
      if (event.type === "message.updated") {
        const properties = getEventProperties(event)
        const info = objectValue(properties?.info) as
          | AssistantInfo
          | undefined

        if (!info || !isAssistantComplete(info)) {
          return
        }

        const messageID = stringValue(info.id)

        if (!messageID || completedMessages.has(messageID)) {
          return
        }

        completedMessages.add(messageID)

        const sessionID = stringValue(info.sessionID) ?? "unknown"
        const agent = getAgent(info)

        if (!isJPAgent(agent)) {
          return
        }

        const provider = stringValue(info.providerID) ?? "unknown"
        const model = stringValue(info.modelID) ?? "unknown"

        const result =
          info.error !== undefined
            ? "error"
            : escalatedMessages.has(messageID)
              ? "escalate"
              : "complete"

        const parentSessionID = getParentSession(sessionID)

        await writeJsonLine(ROUTING_LOG, {
          event: "generation.completed",
          message_id: messageID,
          session_id: sessionID,
          parent_session_id: parentSessionID,
          family: classifyFamily(agent),
          agent,
          tier: classifyTier(agent),
          provider,
          model,
          result,
          duration_ms: getDurationMs(info),
          cost_usd: numberValue(info.cost),
          tokens: {
            input: numberValue(info.tokens?.input),
            output: numberValue(info.tokens?.output),
            reasoning: numberValue(info.tokens?.reasoning),
            cache_read: numberValue(info.tokens?.cache?.read),
            cache_write: numberValue(info.tokens?.cache?.write),
          },
        })

        /*
         * If a Lite agent requested escalation, remember it against
         * the parent session. The next delegated JP agent from that
         * parent can be recorded as the escalation destination.
         */
        if (
          result === "escalate" &&
          parentSessionID &&
          agent.endsWith("-lite")
        ) {
          pendingEscalations.set(parentSessionID, {
            fromAgent: agent,
            fromSession: sessionID,
            timestamp: Date.now(),
          })
        }

        escalatedMessages.delete(messageID)

        return
      }
    },

    /*
     * Inspect generated text only in memory.
     *
     * We intentionally persist NONE of the generated text.
     * The only information extracted is whether the response contains
     * the escalation protocol marker.
     */
    "experimental.text.complete": async (input, output) => {
      if (/STATUS:\s*ESCALATE/i.test(output.text)) {
        escalatedMessages.add(input.messageID)
      }
    },

    /*
     * Tool metadata
     *
     * Arguments and outputs are intentionally not persisted.
     */
    "tool.execute.before": async (input, output) => {
      startedTools.set(input.callID, Date.now())

      await writeJsonLine(TOOL_LOG, {
        event: "tool.started",
        session_id: input.sessionID,
        tool: input.tool,
        call_id: input.callID,
        directory,
      })

      /*
       * OpenCode's task tool includes the selected subagent in args.
       * We extract only that field; the task prompt is never logged.
       */
      if (input.tool === "task") {
        const targetAgent = extractTaskAgent(output.args)

        if (targetAgent && isJPAgent(targetAgent)) {
          await writeJsonLine(ROUTING_LOG, {
            event: "delegation.started",
            parent_session_id: input.sessionID,
            target_agent: targetAgent,
            target_family: classifyFamily(targetAgent),
            target_tier: classifyTier(targetAgent),
          })

          const pending = pendingEscalations.get(input.sessionID)

          if (pending) {
            /*
             * Ignore stale pending escalations from an old turn.
             */
            const ageMs = Date.now() - pending.timestamp

            if (ageMs <= 30 * 60 * 1000) {
              await writeJsonLine(ROUTING_LOG, {
                event: "escalation.routed",
                parent_session_id: input.sessionID,
                from_session_id: pending.fromSession,
                from_agent: pending.fromAgent,
                to_agent: targetAgent,
              })
            }

            pendingEscalations.delete(input.sessionID)
          }
        }
      }
    },

    "tool.execute.after": async (input) => {
      const startedAt = startedTools.get(input.callID)

      if (startedAt !== undefined) {
        startedTools.delete(input.callID)
      }

      await writeJsonLine(TOOL_LOG, {
        event: "tool.completed",
        session_id: input.sessionID,
        tool: input.tool,
        call_id: input.callID,
        duration_ms:
          startedAt !== undefined
            ? Date.now() - startedAt
            : undefined,
        directory,
      })
    },
  }
}