# Installation Guide (source)

The guide is assembled from real builds, not written from memory. Each host build is logged as it happens; the guide is the cleaned-up path through those logs.

- Effort and tasks: Linear project "Installation Guide (Linux host build)" (TRU-21, TRU-23 to TRU-28).
- First build: [helpy-build-log.md](helpy-build-log.md) (Raspberry Pi 5, Ubuntu 26 LTS, clean install).
- Verification step of the guide: the `truemotive-instance-sanity` skill, then the [punch list](../punch-list/MATRIX.md).

## Outline (TODO: fill from the log)

1. Hardware and prerequisites (Pi 5, power, cooling, boot media). TODO
2. Operating system install and first boot. TODO
3. Docker Engine and the `docker` group. Started in the log.
4. Join the tailnet; enable HTTPS certificates; SSH keys. TODO
5. Get the stack: mediamesh checkout, `.env`, pinned TMD tag. TODO
6. Choose the stack shape for the host (full or reduced). TODO
7. Edge overlay and `tailscale serve`. TODO
8. Verify: sanity check, then the manual punch-list rows. TODO
9. Troubleshooting (from the log's surprises). TODO

## Rules for the log

- One entry per step: the command, the result, and anything surprising.
- Mark each entry **reported** (Chris said it was done) or **verified** (checked on the host).
- Never write secret values.
