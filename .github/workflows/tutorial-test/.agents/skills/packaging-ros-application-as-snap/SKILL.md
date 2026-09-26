---
name: packaging-ros-application-as-snap
description: Known-acceptable deviations for the "Tutorial 1: Packaging our first ROS application as a snap" tutorial test. Use these to avoid re-reporting behaviour that is expected and intentional.
---

# Known deviations: Tutorial 1 — Packaging our first ROS application as a snap

## Intended audience

This tutorial is meant for readers with **no prior snap knowledge** — it
introduces every snap concept from scratch. Do not report a step as a finding
simply because it explains or spells out basic snap commands; that hand-holding
is intentional.

However, **basic ROS 2 knowledge is assumed**. The tutorial does not explain ROS
2 concepts (nodes, topics, launch files, `colcon`, `ros2 launch`, etc.). A step
that relies on ROS 2 familiarity without explaining it is **expected**, not a
finding. Report a finding only if the missing knowledge is *snap-related* (which
the tutorial promises to teach) or if a step is wrong/misleading for a reader
who already knows basic ROS 2.

## Scope of known deviations

The following behaviours are **expected** and must **not** be reported as
findings when testing this tutorial. If the tutorial is later updated to fix
one of these, remove the corresponding entry.

## Shared-memory permission error is expected

When the strictly-confined snap runs, it prints errors such as:

```text
[talker-1] ... [RTPS_TRANSPORT_SHM Error] Failed to create segment ...: Permission denied -> Function compute_per_allocation_extra_size
[talker-1] ... [RTPS_MSG_OUT Error] Permission denied -> Function init
```

This is intentional: the tutorial itself documents this error and explains that
ROS 2 falls back to the UDP network transport and that messages are still
exchanged. The step **succeeds** as long as `Publishing: 'Hello World: ...'` and
`I heard: [Hello World: ...]` lines appear. Do not report the
`RTPS_TRANSPORT_SHM` / `RTPS_MSG_OUT` permission-denied errors as a problem.

## Snapcraft build backend (LXD / destructive)

The tutorial invokes `snapcraft pack` without specifying a build backend.
Snapcraft's default backend is multipass, which is not available on the
continuous-integration runner. Building with the LXD backend
(`SNAPCRAFT_BUILD_ENVIRONMENT=lxd`) or `--destructive-mode` is the accepted way
to run this tutorial on CI. Do not report "the tutorial does not mention the
build backend" or any multipass-vs-LXD difference as a finding.

## CI runner environment (already prepared)

The test machine is prepared before the agent runs, to mimic a working user
machine. Do **not** report any of the following as a tutorial problem:

- The `runner` user is added to the `lxd` group so `lxc` works; if a plain
  `lxc`/`lxd` command still returns a socket permission error, prefix it with
  `sg lxd -c "..."` (new group membership needs a fresh login shell).
- Hosted runners ship Docker, whose iptables `FORWARD` policy is `DROP`; this
  blocks LXD container networking. The preparation step already adds
  `DOCKER-USER` accept rules for the `lxdbr0` bridge. If `snapcraft pack` (LXD
  backend) fails with "no network access" while creating the instance, this is
  a CI-environment networking concern, not a tutorial defect.
- snapd, snapcraft, and LXD are typically pre-installed; `snap install`
  reporting "already installed" is expected, not a finding.

## Output values that naturally vary

Do not report differences in the following, which vary between runs:

- Timestamps and message counters in talker/listener output.
- Snap revision numbers (for example `(x1)`, `(x9)`) and `refresh-date`.
- PIDs and unit suffixes in `snap logs` / `journalctl` output.
- The ordering of lines in `snap connections`, `snap info`, or `snap help`.
