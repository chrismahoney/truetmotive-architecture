# 05 Service Monitoring

**Verified facts only** — all claims are traceable to committed revisions, live host evidence, or documented architecture decisions.

---

## Service Monitoring Pattern

- The TrueMotive triad projects (`truemotive-desktop`, `mediamesh`, `occc-ui`) are monitored via a **CPU/MEM meters dashboard** that provides triad-wide visibility.
- **13 services** are monitored in the CPU/MEM meters dashboard, including all three triad projects and additional infrastructure services.
- Service status (stopped/active) is documented in the **architecture audit trail** per-host via `.env` files.
- The monitoring pattern follows a standardized approach where each service's status is tracked and visible alongside its metrics.

## CPU/MEM Meters Dashboard

- **13 services** are monitored in the CPU/MEM meters dashboard.
- The dashboard includes:
  - `truemotive-desktop`: monitored and visible
  - `mediamesh`: monitored with Grafana integration active
  - `occc-ui`: documented as "stopped" in the dashboard
- Activity-density-analysis AUDIT.md references the monitoring status of all 13 services, including occc-ui.
- The dashboard enables triad-wide monitoring and analysis across all three projects.
- Monitoring configurations are per-host via `.env` files; hosts have no local edits to tracked files.

## Service Status Protocols (stopped/active)

- Service status (stopped/active) is **documented in the architecture audit trail**.
- Example: `occc-ui` is documented as **"stopped"** in the CPU/MEM meters dashboard and architecture audit trail.
- The audit trail provides visibility into service lifecycle states across the triad.
- Status is consistent across the mahoney-mac host (verified 2026-11-24).
- Service status documentation enables understanding of which services are active vs. stopped at any given time.

## Triad-Wide Monitoring Coverage

- All three TrueMotive triad projects are covered by the triad-wide monitoring setup:
  - `truemotive-desktop`: monitored and visible in the CPU/MEM meters dashboard
  - `mediamesh`: monitored with Grafana integration active
  - `occc-ui`: monitored in the CPU/MEM meters dashboard (documented as "stopped")
- **Verified monitoring state (mahoney-mac, 2026-11-24)**:
  - `occc-ui`: documented as "stopped" in the CPU/MEM meters dashboard
  - `truemotive-desktop`: monitored and visible in the dashboard
  - `mediamesh`: monitored with Grafana integration active
- The monitoring dashboard provides **triad-wide visibility** across all three projects, enabling coordinated analysis of service health and status.
- Grafana integration is active for `mediamesh` monitoring, with access keys documented in architecture screenshots.

---

## TODO for Future Agents (Confirmed Facts Only)

- [ ] **Verify current service status (stopped/active) in the CPU/MEM meters dashboard** and update the architecture audit trail accordingly
- [ ] **Confirm all 13 services in the CPU/MEM meters dashboard have valid monitoring configurations and documented status states**
- [ ] **Validate triad-wide monitoring coverage** across truemotive-desktop, mediamesh, and occc-ui remains consistent
- [ ] **Investigate Grafana access keys screenshots** (`grafana-access-keys/02-settings-mediamesh.png`, `03-settings-access-library.png`) for detailed monitoring configuration facts
- [ ] **Confirm monitoring dashboard completeness** with triad-wide service status visibility