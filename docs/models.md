# Model Strategy

JP OpenCode can use three independent model pools.

## OpenCode Zen Free

Used for high-volume, low-risk LITE tasks.

Current candidates:

- Muse Spark 1.3 Free
- Ling 3.0 Flash Fin Free
- Nemotron 3.5 Lightning Free
- Nemotron 3 Ultra Free
- MiMo V2.5 Free
- Big Pickle

## OpenCode Go

Primary daily-use provider.

Candidates include:

- GPT-5.6 Luna
- GLM-5.3
- GLM-5.3 Flash
- Qwen3.8 Flash
- Qwen3.8 Max
- Qwen3.7 Plus
- DeepSeek V4 Flash
- DeepSeek V4 Pro
- Kimi K2.7 Code
- MiMo V2.5
- MiMo V2.5 Pro
- MiniMax M3
- others

## OpenAI / Codex

Reserved primarily for expensive tasks where quality materially matters.

Current roles:

- GPT-5.6 Sol -> architecture / high-value reasoning
- GPT-5.6 Terra Fast -> difficult implementation
- other Codex models -> fallback / benchmarking

---

# Initial Code Profile

| Agent | Model |
|---|---|
| Code Orchestrator | OpenCode Go / GPT-5.6 Luna |
| Explorer Lite | Zen / Muse Spark 1.3 Free |
| Explorer Full | TBD benchmark |
| Architect | Codex / GPT-5.6 Sol |
| Designer Lite | TBD |
| Designer Full | TBD |
| Coder Lite | TBD |
| Coder Full | Go / Kimi K2.7 Code candidate |
| Coder Heavy | Codex / GPT-5.6 Terra Fast |
| Reviewer Lite | TBD |
| Reviewer Full | Go / GPT-5.6 Luna |
| Tester | Zen Free candidate |