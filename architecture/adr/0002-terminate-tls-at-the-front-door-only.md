---
status: accepted
---

# TLS ends at the front door; everything behind it is plain HTTP on the host

`tailscale serve` is the only thing that holds a certificate. It terminates TLS with the host's `*.mastodon-adder.ts.net` name, adds the tailnet identity headers, and forwards HTTP to the proxy on `127.0.0.1`. The proxy and every container behind it speak plain HTTP over loopback and the Docker network.

**Why.** There is one certificate to keep alive and tailscaled renews it. Identity headers only exist when `tailscale serve` terminates TLS; a TCP passthrough to the proxy would get the certificate in NPM and lose identity. A single host's Docker network is one trust boundary, so encrypting between containers on the same machine adds renewal work without adding protection.

**Consequences.**
- Nginx Proxy Manager never requests or renews certificates (no Let's Encrypt, no Cloudflare DNS challenge). If a "SSL" row in NPM is set, that is a mistake.
- The proxy's HTTP port is published on `127.0.0.1` only. Anything that can reach it directly can forge identity headers, so it must never be bound to `0.0.0.0`.
- "The tailnet certificate works all the way down" means: the browser shows the valid tailnet certificate for every path, and each path reaches the right container. It does not mean the certificate is present inside every hop.
- Cost of reversing: moving to certificates inside NPM would drop tailnet identity unless a second mechanism is added.
