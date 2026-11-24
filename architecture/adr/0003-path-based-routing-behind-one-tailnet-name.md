---
status: accepted
---

# Path-based routing behind each host's single tailnet name

Each host has exactly one MagicDNS name, so NPM has one proxy host for that name and routes by path (`/`, `/tv/`, and so on) using locations. We rejected `web.<host>`-style subdomains because they cannot get a valid certificate under a tailnet name, and Tailscale Services (extra names) because they add an admin dependency for no gain yet. Every service that is given a path must work under a path prefix; a service that cannot is exposed another way or not at all.
