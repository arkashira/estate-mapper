# tech-spec.md

## 1. Stack

| Layer | Choice | Rationale |
|---|---|---|
| Language | **Go 1.22** (collector agent + API) | Single static binary, cross-compiles for Linux/Windows legacy hosts, no runtime deps on ancient VMs. Goroutines fit fan-out network/log polling. |
| Secondary | **Python 3.12** (inference/ranking service) | Owner-attribution + decommission-risk scoring use pandas/scikit-learn; isolated as a sidecar so the agent stays dependency-free. |
| API framework | Go **chi** (HTTP router) + **sqlc** for typed queries | Minimal, no heavy ORM; sqlc generates type-safe SQL against Postgres. |
| Inference framework | **FastAPI** + **scikit-learn 1.5** + **NetworkX** | NetworkX builds the host↔service↔identity graph; sklearn for usage-clustering & owner classification. |
| Frontend | **SvelteKit** (static adapter) + Tailwind | Report UI is read-heavy dashboards + ranked tables; ships as static assets, no SSR cost. |
| Datastore | **PostgreSQL 16** (+ `pg_trgm`, `timescaledb` opt) | Relational asset graph + time-series telemetry rollups in one engine. |
| Queue | **Postgres `LISTEN/NOTIFY` + `pgmq`** | Avoid standing up Kafka/Redis for v1; discovery jobs are minutes-cadence, not ms. |

**Explicit non-goals v1:** no agent for macOS estates, no SaaS-app discovery (SSPM), no live config remediation — read-only inventory + risk scoring only.

## 2. Hosting (free-tier-first)

| Component | Platform | Free-tier fit |
|---|---|---|
| API + inference service | **Fly.io** (2× shared-cpu-1x, 256MB) | 3 free VMs; runs Go API + Python sidecar in one app via multi-process. |
| Postgres | **Neon** (free: 0.5GB, autosuspend) → **Supabase** at scale | Branchable DB for per-customer demo envs; pgmq + timescaledb available. |
| Collector agent | **Customer-hosted** (self-installed binary) | Runs inside the estate (it MUST — it reads internal AD/SAN/netflow). We never host it. |
| Frontend | **Cloudflare Pages** | Unlimited static, free; serves SvelteKit build + report exports. |
| Object storage (raw log bundles) | **Cloudflare R2** (10GB free, zero egress) | Stores uploaded telemetry snapshots for re-scoring. |
| Secrets/control plane | **Fly secrets** + **Doppler** (free 3-seat) | Per-tenant collector enrollment tokens. |

**Topology:** the *collector agent* is on-prem (pull-only, outbound TLS to API); the *control plane* (API/inference/UI) is the hosted SaaS. No inbound ports opened in the customer estate.

## 3. Data Model

**`assets`** — discovered hosts/VMs
`id (uuid pk)`, `tenant_id`, `hostname`, `fqdn`, `ip_primary inet`, `ip_all inet[]`, `mac`, `os_family`, `os_version`, `virtualization (vmware|hyperv|kvm|bare-metal|unknown)`, `hypervisor_host`, `cpu_cores`, `ram_mb`, `disk_gb`, `power_state`, `first_seen`, `last_seen`, `discovery_source (arp|netflow|vcenter|ad|cmdb|scan)`, `confidence numeric`

**`services`** — listening services per asset
`id`, `asset_id fk`, `port`, `proto`, `service_name`, `process`, `banner`, `tls_cn`, `last_active`, `bytes_in_30d`, `bytes_out_30d`, `distinct_peers_30d`

**`identities`** — users/service accounts (from AD/auth logs)
`id`, `tenant_id`, `principal`, `kind (user|svc_account|computer)`, `dept`, `manager`, `last_logon`, `enabled bool`, `source (ad_ldap|auth_log|kerberos)`

**`edges`** — graph relations (typed)
`id`, `tenant_id`, `src_id`, `src_type`, `dst_id`, `dst_type`, `relation (talks_to|authenticates_as|hosts|depends_on|owned_by)`, `weight`, `observed_count`, `first_seen`, `last_seen`

**`usage_signals`** — time-series rollups (timescale hypertable)
`asset_id`, `bucket timestamptz`, `cpu_pct`, `net_bytes`, `auth_events`, `unique_sessions`, `interactive_logons`

**`owner_attributions`** — inferred ownership
`asset_id`, `identity_id`, `score numeric`, `method (logon_freq|svc_acct_bind|ad_description|netflow_dominant|manual)`, `evidence jsonb`, `rank`

**`risk_assessments`** — the deliverable
`id`, `asset_id`, `verdict (safe_decom|migrate|investigate|keep)`, `risk_score numeric(0-100)`, `usage_score`, `dependency_score`, `owner_clarity_score`, `blast_radius int`, `rationale jsonb`, `generated_at`, `model_version`

**`tenants`**, **`collectors`** (`enrollment_token_hash`, `last_checkin`, `agent_version`, `scopes`), **`audit_log`**.

## 4. API Surface

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/v1/collectors/enroll` | Agent exchanges one-time enrollment token for a scoped mTLS client cert + collector_id. |
| `POST` | `/v1/ingest/batch` | Collector pushes compressed discovery batch (assets/services/edges/signals); idempotent by content hash. |
| `GET` | `/v1/assets?verdict=&owner=&q=` | Filterable, paginated asset inventory with current risk verdict. |
| `GET` | `/v1/assets/{id}/graph` | Dependency subgraph (N-hop) for blast-radius visualization. |
| `GET` | `/v1/assets/{id}/owners` | Ranked owner attributions + evidence trail. |
| `POST` | `/v1/assets/{id}/feedback` | Human override (confirm owner / mark keep) — feeds retraining + drops risk on FP. |
| `POST` | `/v1/scoring/run` | Trigger (re)scoring for a tenant; returns job id. |
| `GET` | `/v1/reports/decommission?format=csv\|pdf\|json` | The headline deliverable: ranked safe-to-decommission / migration-risk list. |
| `GET` | `/v1/collectors` | Fleet health: last check-in, agent version, scope, data freshness. |
| `GET` | `/v1/audit?since=` | Tamper-evident audit log of reads/exports (compliance requirement for asset data). |

All endpoints `tenant_id`-scoped via cert/JWT claims; ingest is the only high-volume path (batched, gzip, 202-async).

## 5. Security Model

- **Collector ↔ control plane:** mutual TLS. Enrollment is one-time-token → per-collector client cert (90-day rotation). Collector holds **read-only** estate credentials; principle is "agent can see, never change."
- **Estate credentials stay local:** AD bind creds, vCenter API keys, SSH keys for log scrape live **only** in the on-prem collector's OS keystore (Windows DPAPI / Linux `libsecret`), never transit to SaaS. We ingest *derived facts*, not raw credentials.
- **User auth (UI/API):** OIDC (Auth0 free tier / WorkOS) → short-lived JWT. RBAC roles: `viewer`, `analyst`, `admin`. Decommission-report export gated to `analyst+` and always audit-logged.
- **Secrets:** Doppler/Fly secrets for control-plane; no secrets in repo, `.env.example` only. Enrollment tokens stored as Argon2id hashes.
- **Data sensitivity:** asset inventory + owner maps are recon-grade intel — encrypt at rest (Neon/R2 SSE), TLS 1.3 in transit, per-tenant row-level security (Postgres RLS) as defense-in-depth.
- **IAM (cloud):** least-privilege service identities per component; inference sidecar has no DB write on raw ingest tables, only on `risk_assessments`/`owner_attributions`.
- **Blast-radius of a breach:** even full control-plane compromise yields metadata + inferred ownership, **not** a foothold into the customer estate (no inbound path, no stored estate creds).

## 6. Observability

- **Logs:** structured JSON (slog in Go, structlog in Python) → stdout → Fly → **Grafana Loki** (free tier / self-host on Fly). Mandatory fields: `tenant_id`, `collector_id`, `trace_id`, `batch_hash`.
- **Metrics:** Prometheus exposition → **Grafana Cloud free** (10k series). Golden signals: `ingest_batch_latency`, `assets_discovered_total`, `scoring_run_duration`, `collector_checkin_age` (alert > 2× expected cadence), `attribution_confidence_p50`.
- **Traces:** **OpenTelemetry** SDK, OTLP → Grafana Tempo. Span the ingest→normalize→graph-build→score pipeline; trace_id propagated from collector batch header.
- **Product-health SLOs:** data freshness < 1h for active collectors; scoring run < 5 min for 10k assets; false-positive rate on `safe_decom` < 2% (tracked via feedback endpoint).
- **Audit ≠ observability:** `audit_log` is durable in Postgres (compliance), separate from operational logs (ephemeral in Loki).

## 7. Build / CI

- **Monorepo** (`/collector`, `/api`, `/inference`, `/web`), managed with a `Taskfile.yml`.
- **CI: GitHub Actions** (free for the public/lightweight repo):
  - `lint`: `golangci-lint`, `ruff`, `svelte-check`.
  - `test`: Go unit + `testcontainers-go` against ephemeral Postgres; Python pytest; coverage gate ≥ 70%.
  - `build`: cross-compile collector for `linux/amd64`, `windows/amd64`, `linux/arm64`; embed version via ldflags; produce SBOM (`syft`).
  - `scan`: `govulncheck`, `trivy` (image + SBOM), `gitleaks` — hard-fail on high CVE or leaked secret.
  - `release`: tagged → GoReleaser signs binaries (cosign) + publishes checksummed collector artifacts to GitHub Releases (customers verify before on-prem install).
- **Deploy:** `fly deploy` (API+inference) and Cloudflare Pages (web) on merge to `main`; DB migrations via `golang-migrate`, run as a pre-deploy release command.
- **Collector distribution:** signed binary + `install.sh`/MSI; auto-update opt-in, checks signature against pinned cosign public key.