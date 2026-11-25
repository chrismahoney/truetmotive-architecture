# USER_INPUT.md

## Services

### Portainer

#### Access Tokens
- Turbo: ptr_CdfHCEaN114v5wGbcPlw399r9iurgRiNMNtBnfELtbw=
- Helpy: TBD
- Mahoney-Mac:

### Portainer Data Retrieval

#### Pre-task setup
export PT_HOST=turbo
export PT_PORT=9443
export PT_API_KEY="ptr_CdfHCEaN114v5wGbcPlw399r9iurgRiNMNtBnfELtbw="
export STACK_NAME="mediamesh"
export STACK_FILE_URL="https://$PT_HOST:$PT_PORT/api/stacks?type=2&searchText=$STACK_NAME"

#### Access: Stack Compose file:
echo "Retrieve Stack Config: $STACK_FILE_URL"

curl -sk -H "X-API-Key: $PT_API_KEY" \
  "https://$PT_HOST:$PT_PORT/api/stacks?type=2&searchText=$STACK_NAME" > $STACK_NAME-compose.yml

#### Access: Everything on turbo
for ep in stacks endpoints users teams roles registries settings webhooks; do
  curl -sk -H "X-API-Key: $PT_API_KEY" "https://$PT_HOST:$PT_PORT/api/$ep" > "$ep.json"
done

#### Optional: Backup: Official method
This backs up everything via the volume containing the SQLite db and local storage.

```
docker run --rm -v portainer_data:/data -v "$PWD":/backup alpine \
  tar czf /backup/portainer-backup.tgz -C /data .
```

## Ports

### mahoney-mac.mastodon-adder.ts.net (OLD DEV)
- 8888: engine:/api

### helpy.mastodon-adder.ts.net (TEST)
- ????: engine:/api

### turbo.mastodon-adder.ts.net (INT PROD)
- 

## Links
- Landing Page
  - TEST TS Host (helpy.mastodon-adder.ts.net)
    - https://helpy.mastodon-adder.ts.net
      - Says 'not on tailnet' blocked
  - TEST CF Host (helpy.truemotive.cloud)
    - http://helpy.truemotive.cloud
      - NPM 'Congrats' page
    - https://helpy.truemotive.cloud
      - "Unrecognized SSL name" browser error

- MCP Server
    - http://mahoney-mac.mastodon-adder.ts.net:8888/mcp
      - Offline
    - http://turbo.mastodon-adder.ts.net:8888/mcp

### Turbo
- API: 
- MCP SSE URL: http://mahoney-mac.mastodon-adder.ts.net:8888/mcp
- Landing Page: 
- Tailscale Serve?

## Instance-specific

### Turbo
MCP Link: http://mahoney-mac.mastodon-adder.ts.net:8888/mcp




Graph failed attempt at mahoney-mac:
https://mahoney-mac.mastodon-adder.ts.net/embed/graph/active-knowledge-spooky-live-breakout-1?theme=studio&mode=dark
