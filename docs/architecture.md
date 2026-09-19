# AetherOS architecture

```
[ user intent ]
       |
       v
[ Aether Supervisor ]  <-- the “OS is an AI” layer
       |
       +--> planner (goals → DAG of actions)
       +--> policy  (what is allowed)
       +--> memory  (what the machine has done)
       |
[ service fabric ]     <-- replaces init / pkg / scheduler over time
       |
[ Linux kernel ]       <-- stay here for a long time
       |
[ hardware / QEMU / AVD ]
```

## Design rules

1. **Capability, not prompt.** The model proposes. A tiny deterministic kernel of rules executes.
2. **Replace outward-in.** Apps → daemons → init → modules → kernel.
3. **Always bootable without the model.** If the AI is down, a static policy must still start a shell.
4. **Guest first.** Break things in QEMU, not on a phone you need tomorrow.

## Components

### Supervisor
Python prototype in `aios/supervisor.py`. Later: Rust service with a frozen policy file.

### Intent language
Plain English now. Later a small structured language:

```
GOAL capture-photo
NEED camera, storage
THEN ocr
THEN append notes
```

### Isolation
Every AI-spawned job runs with:
- seccomp filter generated from the plan
- cgroup memory/cpu cap
- no raw disk unless the policy file says so
