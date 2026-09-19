#!/usr/bin/env python3
"""AetherOS userspace supervisor — Phase 2 prototype.

This is not a kernel. It turns a goal into a plan and pretends to dispatch
jobs the way an AI-native OS would. Wire it to real processes later.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone


@dataclass
class Action:
    name: str
    capability: str
    command: list[str]
    why: str


def plan(intent: str) -> list[Action]:
    text = intent.lower()
    actions: list[Action] = [
        Action(
            "acknowledge",
            "log",
            ["aios-log", intent],
            "Every goal is recorded before anything runs.",
        )
    ]
    if any(w in text for w in ("note", "write", "remember")):
        actions.append(
            Action(
                "store-note",
                "storage",
                ["aios-notes", "append", intent],
                "Notes are a first-class OS object, not an app.",
            )
        )
    if any(w in text for w in ("photo", "camera", "picture")):
        actions.append(
            Action(
                "capture",
                "camera",
                ["aios-camera", "still"],
                "Camera is a capability the supervisor grants, not an icon.",
            )
        )
    if any(w in text for w in ("lab", "status", "alive")):
        actions.append(
            Action(
                "health",
                "sys",
                ["aios-health"],
                "The OS reports itself; nothing is a black-box settings app.",
            )
        )
    if len(actions) == 1:
        actions.append(
            Action(
                "unparsed-goal",
                "shell",
                ["aios-ask", intent],
                "Unknown intent stays queued instead of silently failing.",
            )
        )
    return actions


def dispatch(actions: list[Action]) -> dict:
    # Dry-run only. Real spawn + seccomp comes in Phase 3.
    return {
        "ts": datetime.now(timezone.utc).isoformat(),
        "pid1": "linux-init (not yet replaced)",
        "kernel": "linux (not yet replaced)",
        "actions": [asdict(a) for a in actions],
        "note": "Dry-run. No processes spawned. This is the AI OS control plane.",
    }


def main() -> int:
    intent = " ".join(sys.argv[1:]).strip() or "status of the lab"
    result = dispatch(plan(intent))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
