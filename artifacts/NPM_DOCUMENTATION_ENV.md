# Nginx Proxy Manager Migration Result

## Installation Validation ✅

The nginx proxy manager (NPM) installation has been successfully validated and is operational across the Mediamesh stack.

### Configuration Summary

- **NPM Config File:** `nginx/config.json` with 10 server blocks
- **Services Proxied:** engine, web, spacecom, mediamtx, occc-ui, mediamtx-connect, livekit, truemotive-fallback, truemotive-cockpit, decisions-redirect
- **TLS Termination:** Pre-issued Tailscale certificates from `tailscale/certs/`
- **Port Mappings:** Preserved (443 HTTPS, 8443-8455)
- **Admin UI:** Accessible on port 81 (HTTP) with `NPM_ADMIN_PASSWORD=SecurePass123!`

### Files Modified

| File | Change |
|------|--------|
| `nginx/config.json` | Created - NPM configuration with 10 server blocks |
| `docker-compose.yml` | Replaced Caddy service with nginx-proxy-manager |
| `.env` | Removed `TS_AUTHKEY`, added `NPM_ADMIN_PASSWORD=SecurePass123!` |
| `plans/NPM_REFACTOR.md` | Comprehensive migration plan documentation |
| `docs/artifacts/NPM_REFACTOR_PASS1.md` | Pass 1 results confirming migration |

### SSL/TLS Configuration

#### Tailscale Pre-issued Certs

- Certificates are issued via `tailscale cert` on the host
- Mounted read-only from `./tailscale/certs/` → `/etc/nginx/certs/`
- NPM uses `ssl: "advanced"` mode with these pre-provisioned certs
- No ACME/Let's Encrypt required - certs already exist

#### Certificate Paths

```
Host:       ./tailscale/certs/          (read-only mount)
Container:  /etc/nginx/certs/           (NPM reads from here)
NPM config: ssl: "advanced"           (references the mounted certs)
```

#### Environment-Specific SSL Setups

1. **`helpy` (Pi 5) - Primary Production:**
   - NPM owns ports 80/443
   - Caddy parked behind NPM `caddy` profile (opt-in only)
   - TrueMotive container on NPM `truemotive` network
   - Tailscale auth via `sidecars/tailscale-nginx-auth` sidecar
   - `auth_request` to validate Tailscale login headers

2. **Main Development Stack:**
   - Caddy service disabled (`profiles: ["caddy"]`)
   - NPM is the default front-door reverse proxy
   - All 10 services accessible through NPM on 443/8443-8455
   - Tailscale identity headers passed through via `proxy_set_header`

3. **Tailnet vs. Non-Tailnet Access:**
   - **Tailnet visitors:** `auth_request` to `tailscale-nginx-auth` → 200 if logged in, 401 if not
   - **Non-tailnet:** Falls back to `:4715` token-only listener, shows access/sign-in page
   - `Tailscale-User-Login`, `Tailscale-User-Name`, `X-TMD-Proxy-Secret` headers forwarded to API

### Success Criteria ✅

- [x] NPM container running and reachable via tailnet hostname on port 443/8443
- [x] All 10 services proxyable through NPM
- [x] Tailscale identity headers passing through to API (verified via health check endpoints)
- [x] HLS/streaming working through NPM (same segments served at same URLs)
- [x] All existing URLs continue to work (same port map, same hostnames)
- [x] No Caddy-specific env vars (`TS_AUTHKEY`) in `.env`
- [x] `truemotive.mastodon-adder.ts.net` hostname eliminated from active configuration
- [x] `TRUEMOTIVE_TAILNET_HOST=turbo-1.mastodon-adder.ts.net` used through nginx Proxy Manager

### Next Steps - SSL Environment Setup

#### 1. Certificate Renewal/Refresh

```bash
# Regenerate Tailscale certs on host when they expire
tailscale cert --expire 87600h  # 10 years from now

# Restart NPM to pick up new certs
docker restart nginx-proxy-manager
```

#### 2. Per-Environment SSL Configuration

**helpy (Pi 5):**
- Ensure `tailscale/certs/` directory has current certs
- Verify `tailscale serve --https=443 http://127.0.0.1:10848` is running
- NPM host `helpy.mastodon-adder.ts.net` → valid cert auto-used

**Development/Local:**
- Use `http://localhost:8181` for NPM admin UI
- Or `http://<host-ip>:8080` for direct NPM access
- Certs still from `tailscale/certs/` but may need `127.0.0.1` SAN

**New Host Instances:**
1. Issue wildcard cert: `tailscale cert *.mastodon-adder.ts.net`
2. Add NPM host in NPM web UI or `config.json`:
   - Domain: `app.<instance>.truemotive.xyz`
   - Target: `<service>:<port>` on the `truemotive` network
   - SSL: advanced, use existing certs from `tailscale/certs/`
3. Configure `auth_request` for Tailscale gate if needed

#### 3. Tailscale Auth Header Flow

```
Client --> NPM (ssl termination) --> auth_request --> tailscale-nginx-auth
                                                                |
                                                                v
                                              Returns 200/401 with Tailscale headers
                                                                |
                                                                v
                                              NPM proxies to TrueMotive service
                                                                |
                                                                v
                                              API reads: req.headers['Tailscale-User-Login']
```

#### 4. Debugging SSL/TLS Issues

```bash
# Verify NPM is running and certs are mounted
docker exec nginx-proxy-manager ls -la /etc/nginx/certs/

# Test SSL connectivity
curl -v https://turbo-1.mastodon-adder.ts.net:8453

# Check Tailscale status on host
tailscale status

# Verify headers are passed through
curl -H "Tailscale-User-Login: test" https://turbo-1.mastodon-adder.ts.net:8453/api/gate
```

### Artifacts

- `docs/artifacts/NPM_REFACTOR_PASS1.md` - Pass 1 migration results
- `plans/NPM_REFACTOR.md` - Comprehensive migration plan
- `nginx/config.json` - NPM configuration file
