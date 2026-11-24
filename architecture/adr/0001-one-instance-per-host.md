---
status: accepted
---

# One instance per host, each with its own front door and proxy

An instance is everything on one physical host: containers, database, proxy and front door. We chose this over a shared proxy on helpy because a shared proxy makes helpy a single point of failure and cannot reach each host's loopback. The environments are `dev` (mahoney-mac), `test` (helpy) and `prod` (turbo-1). Environments never depend on each other.
