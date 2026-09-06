#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


STATE_DIR = Path.home() / ".local" / "state" / "jp-opencode"
ROUTING_LOG = STATE_DIR / "logs" / "routing.jsonl"


def load_events() -> list[dict[str, Any]]:
    if not ROUTING_LOG.exists():
        return []

    events: list[dict[str, Any]] = []

    with ROUTING_LOG.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()

            if not line:
                continue

            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue

            if isinstance(value, dict):
                events.append(value)

    return events


def generation_events(
    events: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        event
        for event in events
        if event.get("event") == "generation.completed"
    ]


def escalation_routes(
    events: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        event
        for event in events
        if event.get("event") == "escalation.routed"
    ]


def token_total(event: dict[str, Any]) -> int:
    tokens = event.get("tokens")

    if not isinstance(tokens, dict):
        return 0

    keys = (
        "input",
        "output",
        "reasoning",
        "cache_read",
        "cache_write",
    )

    return sum(
        int(tokens.get(key, 0) or 0)
        for key in keys
    )


def percent(part: int, total: int) -> float:
    if total == 0:
        return 0.0

    return (part / total) * 100


def print_table(
    headers: list[str],
    rows: list[list[str]],
    right_columns: set[int] | None = None,
) -> None:
    if not rows:
        print("No data.")
        return

    right_columns = right_columns or set()

    widths = [
        max(
            len(headers[index]),
            max(len(row[index]) for row in rows),
        )
        for index in range(len(headers))
    ]

    def format_row(row: list[str]) -> str:
        parts: list[str] = []

        for index, value in enumerate(row):
            if index in right_columns:
                parts.append(value.rjust(widths[index]))
            else:
                parts.append(value.ljust(widths[index]))

        return "  ".join(parts)

    print(format_row(headers))
    print(
        "  ".join(
            "-" * width
            for width in widths
        )
    )

    for row in rows:
        print(format_row(row))


def summary(
    generations: list[dict[str, Any]],
    routes: list[dict[str, Any]],
) -> None:
    total = len(generations)

    if total == 0:
        print("No routing data recorded yet.")
        return

    escalations = sum(
        event.get("result") == "escalate"
        for event in generations
    )

    errors = sum(
        event.get("result") == "error"
        for event in generations
    )

    total_tokens = sum(token_total(event) for event in generations)

    total_cost = sum(
        float(event.get("cost_usd", 0) or 0)
        for event in generations
    )

    providers = Counter(
        str(event.get("provider", "unknown"))
        for event in generations
    )

    models = Counter(
        str(event.get("model", "unknown"))
        for event in generations
    )

    families = Counter(
        str(event.get("family", "unknown"))
        for event in generations
    )

    print("Summary")
    print("-------")
    print(f"Generations:       {total}")
    print(f"Escalations:       {escalations}")
    print(f"Escalation rate:   {percent(escalations, total):.1f}%")
    print(f"Errors:            {errors}")
    print(f"Recorded tokens:   {total_tokens:,}")
    print(f"Recorded cost:     ${total_cost:.6f}")
    print(f"Escalation routes: {len(routes)}")

    print()
    print("Families")
    print("--------")

    for family, count in families.most_common():
        print(
            f"{family:<12} "
            f"{count:>6} "
            f"({percent(count, total):>5.1f}%)"
        )

    print()
    print("Top models")
    print("----------")

    for model, count in models.most_common(5):
        print(
            f"{model:<32} "
            f"{count:>6} "
            f"({percent(count, total):>5.1f}%)"
        )

    print()
    print("Providers")
    print("---------")

    for provider, count in providers.most_common():
        print(
            f"{provider:<18} "
            f"{count:>6} "
            f"({percent(count, total):>5.1f}%)"
        )


def model_stats(generations: list[dict[str, Any]]) -> None:
    grouped: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "calls": 0,
            "escalations": 0,
            "errors": 0,
            "tokens": 0,
            "cost": 0.0,
        }
    )

    for event in generations:
        provider = str(event.get("provider", "unknown"))
        model = str(event.get("model", "unknown"))

        key = f"{provider}/{model}"

        stats = grouped[key]

        stats["calls"] += 1
        stats["tokens"] += token_total(event)
        stats["cost"] += float(event.get("cost_usd", 0) or 0)

        if event.get("result") == "escalate":
            stats["escalations"] += 1

        if event.get("result") == "error":
            stats["errors"] += 1

    total = sum(
        value["calls"]
        for value in grouped.values()
    )

    rows: list[list[str]] = []

    for model, stats in sorted(
        grouped.items(),
        key=lambda item: item[1]["calls"],
        reverse=True,
    ):
        calls = stats["calls"]
        escalations = stats["escalations"]

        rows.append(
            [
                model,
                f"{calls:,}",
                f"{percent(calls, total):.1f}%",
                f"{escalations:,}",
                f"{percent(escalations, calls):.1f}%",
                f"{stats['errors']:,}",
                f"{stats['tokens']:,}",
                f"${stats['cost']:.6f}",
            ]
        )

    print_table(
        [
            "Model",
            "Calls",
            "Share",
            "Esc",
            "Esc %",
            "Errors",
            "Tokens",
            "Cost",
        ],
        rows,
        right_columns={1, 2, 3, 4, 5, 6, 7},
    )


def agent_stats(generations: list[dict[str, Any]]) -> None:
    grouped: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "runs": 0,
            "complete": 0,
            "escalate": 0,
            "error": 0,
            "tokens": 0,
            "duration": [],
        }
    )

    for event in generations:
        agent = str(event.get("agent", "unknown"))
        stats = grouped[agent]

        stats["runs"] += 1
        stats["tokens"] += token_total(event)

        result = str(event.get("result", "unknown"))

        if result in stats:
            stats[result] += 1

        duration = event.get("duration_ms")

        if isinstance(duration, (int, float)):
            stats["duration"].append(float(duration))

    rows: list[list[str]] = []

    for agent, stats in sorted(
        grouped.items(),
        key=lambda item: item[1]["runs"],
        reverse=True,
    ):
        runs = stats["runs"]
        durations = stats["duration"]

        average_duration = (
            sum(durations) / len(durations)
            if durations
            else 0
        )

        rows.append(
            [
                agent,
                f"{runs:,}",
                f"{stats['complete']:,}",
                f"{stats['escalate']:,}",
                f"{percent(stats['escalate'], runs):.1f}%",
                f"{stats['error']:,}",
                f"{average_duration / 1000:.1f}s",
                f"{stats['tokens']:,}",
            ]
        )

    print_table(
        [
            "Agent",
            "Runs",
            "Complete",
            "Esc",
            "Esc %",
            "Errors",
            "Avg",
            "Tokens",
        ],
        rows,
        right_columns={1, 2, 3, 4, 5, 6, 7},
    )


def provider_stats(generations: list[dict[str, Any]]) -> None:
    grouped: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "calls": 0,
            "escalations": 0,
            "tokens": 0,
            "cost": 0.0,
        }
    )

    for event in generations:
        provider = str(event.get("provider", "unknown"))
        stats = grouped[provider]

        stats["calls"] += 1
        stats["tokens"] += token_total(event)
        stats["cost"] += float(event.get("cost_usd", 0) or 0)

        if event.get("result") == "escalate":
            stats["escalations"] += 1

    total = sum(
        value["calls"]
        for value in grouped.values()
    )

    rows: list[list[str]] = []

    for provider, stats in sorted(
        grouped.items(),
        key=lambda item: item[1]["calls"],
        reverse=True,
    ):
        rows.append(
            [
                provider,
                f"{stats['calls']:,}",
                f"{percent(stats['calls'], total):.1f}%",
                f"{stats['escalations']:,}",
                f"{stats['tokens']:,}",
                f"${stats['cost']:.6f}",
            ]
        )

    print_table(
        [
            "Provider",
            "Calls",
            "Share",
            "Esc",
            "Tokens",
            "Cost",
        ],
        rows,
        right_columns={1, 2, 3, 4, 5},
    )


def escalation_stats(
    generations: list[dict[str, Any]],
    routes: list[dict[str, Any]],
) -> None:
    lite_stats: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "runs": 0,
            "escalations": 0,
        }
    )

    for event in generations:
        agent = str(event.get("agent", "unknown"))

        if event.get("tier") != "lite":
            continue

        lite_stats[agent]["runs"] += 1

        if event.get("result") == "escalate":
            lite_stats[agent]["escalations"] += 1

    rows: list[list[str]] = []

    for agent, stats in sorted(
        lite_stats.items(),
        key=lambda item: (
            item[1]["escalations"],
            item[1]["runs"],
        ),
        reverse=True,
    ):
        runs = stats["runs"]
        escalations = stats["escalations"]

        rows.append(
            [
                agent,
                f"{runs:,}",
                f"{escalations:,}",
                f"{percent(escalations, runs):.1f}%",
            ]
        )

    print("Lite escalation rate")
    print("--------------------")

    print_table(
        [
            "Agent",
            "Runs",
            "Escalations",
            "Rate",
        ],
        rows,
        right_columns={1, 2, 3},
    )

    print()
    print("Escalation destinations")
    print("-----------------------")

    destinations = Counter(
        (
            str(event.get("from_agent", "unknown")),
            str(event.get("to_agent", "unknown")),
        )
        for event in routes
    )

    destination_rows = [
        [
            source,
            target,
            f"{count:,}",
        ]
        for (source, target), count in destinations.most_common()
    ]

    print_table(
        [
            "From",
            "To",
            "Count",
        ],
        destination_rows,
        right_columns={2},
    )


def main() -> int:
    events = load_events()

    generations = generation_events(events)
    routes = escalation_routes(events)

    command = sys.argv[1] if len(sys.argv) > 1 else "summary"

    if command == "summary":
        summary(generations, routes)
        return 0

    if command == "models":
        model_stats(generations)
        return 0

    if command == "agents":
        agent_stats(generations)
        return 0

    if command == "providers":
        provider_stats(generations)
        return 0

    if command == "escalations":
        escalation_stats(generations, routes)
        return 0

    print(
        "Usage: stats.py "
        "[summary|models|agents|providers|escalations]",
        file=sys.stderr,
    )

    return 1


if __name__ == "__main__":
    raise SystemExit(main())