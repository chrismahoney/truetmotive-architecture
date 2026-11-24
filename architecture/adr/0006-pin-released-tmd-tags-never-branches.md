---
status: accepted
---

# Hosts pin a TMD release; target is v2.8.2

Hosts build TMD from a tag, never a branch. v2.8.0 was verified in the clean room on 2026-11-24 and is the fallback. The target is **v2.8.2**. 2.8.1 was never released; 2.8.2 carries its changes. The release commit `ea67e119` is truemotive-desktop PR #191. TMD's tags (`vX.Y.Z-beta`) are created only by the Jenkins `truemotive-release` job, which refuses an existing tag, so nobody pushes one by hand. Until the job has run, hosts build from the release commit and the punch-list row A3 stays 🟡. No host moves to a version that has not passed the full punch list in a clean room.
