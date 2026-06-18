```markdown
# Business Model Canvas – estate-mapper
v0.1 ‑ Aligned to Axentx 2026-05-23 pipeline & portfolio

## 1. Key Partners
- **IaaS/PaaS providers** (AWS, Azure, GCP): supply resource inventory APIs and tagging schemas.
- **Enterprise SIEM vendors** (Splunk, Elastic, Wazuh): provide normalized, licensed syslog/netflow datasets used for inference.
- **ITAM/Discovery tools** (ServiceNow ITOM, Flexera, BMC Helix): export CMDB snapshots via REST.
- **Security vendors** (CrowdStrike, Tanium): contribute endpoint telemetry under compatible licenses (Apache-2.0).
- **Open-source IP-edge communities**: ingest gray-literature network diagrams (MPL-2.0) to enrich topological priors.

## 2. Key Activities
- **Agent orchestration & discovery pipeline**
  Repo integration: replicate discovery topology from `arkashira/surrogate-1-harvest` branch (modules: network-scan, telemetry-ingest, auth-log-parser).
  Growth driver: ~144.6 M pairs/7d kept the inference stack fresh; estate-mapper consolidates only the subset required for estate traversal.
- **Telemetry-augmented asset inference**
  Combine training-pairs-leading (61.3 M) for ML priors, pairs-B (31 M) for network adjacency graphs, pairs-D (38.3 M) for anomaly labels.
- **Risk-scoring engine**
  Serialized model weights hosted in BRAIN (pgvector) to maintain incremental learning against new decommission telemetry.
- **Interactive estate visualization & export**
  Use Three.js/MapLibre GL in a React frontend shipped via `arkashira/surrogate-1-harvest` static build artifact.

## 3. Value Propositions
- **Autonomous asset inventory ≠ CMDB duplication**
  Discovers *actual* running VMs, containers, S3 buckets, VDIs, and SaaS subscriptions; ignores CMDB stale entries.
- **Decommission-risk metric** (≥ 1.0 = high confidence safe-to-remove)
  Weighted model combining:
  – 30-day median CPU & memory footprint (telemetry).
  – Outbound egress bytes (network).
  – Authentication frequency (auth logs).
  – License compliance delta (ITAM feeds).
- **Rollback impact assessment**
  If `estate-mapper` flag = migration-risk, export STIG-compatible mitigation SOAR playbook in JSON for ServiceNow or Red Hat Insights.

## 4. Customer Relationships
### Self-serve tiers
- **Explorer (free, full features)**
  Up to 1,000 hosts; usage telemetry feeds BRAIN; aggregated anonymized stats published; limit can be raised via company credit.
- **Steward (paid)**
  Unlimited hosts; SLAs: 24h P1 issues, weekly summary of top-20 migration candidates.
- **Architect Enterprise (custom)**
  On-prem deploy of BRAIN-index for air-gapped estates; quarterly model re-training; dedicated Axentx support channel (`#estate-mapper` in Slack).

### High-touch
- **VMware & OpenShift migration workshops**
  4-hour sessions demonstrating estate-mapper output → vMotion priority queue.
- **Public sector & defense**
  FedRAMP Tailored/IL4 attestation package (STIG artifacts auto-generated).

## 5. Customer Segments
| Segment           | Pain                          | Usage Trigger                          | Willingness-to-Pay         |
|-------------------|-------------------------------|----------------------------------------|----------------------------|
| **Cloud FinOps**  | $2.1B annual idle spend*      | Monthly cost anomaly reports           | $8k/yr Steward tier        |
| **Legacy estate migration** | $18-42M/yr data-center close | Board-approved migration budget        | $25k Architect Enterprise  |
| **M&A due-diligence**     | 30% infra duplication uncovered | CFO mandate post LOI                   | $45k one-off               |
| **Regulated verticals**   | FedRAMP/PCI evidence required  | Compliance audit red-flag              | $12k Explorer + consulting |

\*source: Gartner 2025 public cloud waste report

## 6. Key Resources
- **BRAIN vector store** – enriched with ~144M pairs/7d; index version `estate-mapper-v1`.
- **Supabase Postgres** – hosts graph edges (host-to-service, service-to-tag) and risk matrices.
- **Axentx brand license** – leverages existing `arkashira` GitHub org and verified OSS compliance.
- **Domain experts** – staff architects previously shipped `iceoryx2` (Lemmy programming), bringing real-time IPC expertise to estate telemetry.

## 7. Channels
- **Product-led growth**
  README CTA → `Try it` → free tier auto-provisions instance on Railway (Axentx corporate account).
- **Marketplaces & integrations**
  - **ServiceNow Store**: “Axentx estate-mapper” app listed Q3-2026.
  - **Ansible Galaxy**: `axentx.estate_mapper` role for auto-discovery on first run.
- **Content & SEO**
  Weekly blog “Decommission Tier List: top 5 instances to kill next quarter” drives organic to GitHub repo; mirrored on Lemmy community.
- **Conference circuit**
  KubeCon, ConfigMgmtCamp, HashiTalks.

## 8. Cost Structure
### Variable
- **Compute / GPU**
  – vLLM inference: ~0.7 A100-h per 1,000 hosts.
  – BRAIN vector search: p99 latency < 80 ms at 10k QPS (Supabase Pro).
- **Data egress**
  – Ingest ~2 TB/day from syslog / netflow.
- **OSS licensing**
  – All third-party datasets compatible with Apache-2.0, MIT, CC-BY-4.0.
  – In-house weight updates MIT licensed back to community.

### Fixed
- **GitHub Enterprise** – org seat + Actions minutes.
- **Railway / Supabase Pro** – staging & prod run-time.
- **Axentx legal & FedRAMP compliance** – $60k/yr retainer.

## 9. Revenue Streams
| Stream             | Price Point | Recurrence | Alignment           |
|--------------------|-------------|------------|---------------------|
| SaaS Steward tier  | $8k/year    | Annual     | Usage-based credits |
| Enterprise license | $25k/yr     | Annual     | Named seats         |
| One-time workshop  | $4k–$6k     | Per event  | Delivery margin     |
| Data insights report* | $1.5k   | One-off     | CxO stakeholders    |

\*Synthetic 1-pager “Dup-to-Clean” report derived from estate-mapper JSON export.

## 10. Exit & Portfolio Extension Signals
- ** gate validated **: > 5 paying logos within 90 days OR > $50k ACV in pipeline.
- **BMC adaptation**: if VMware & bare-metal converged estates (e.g., Proxmox) exceed 60% of total leads, spin out `estate-mapper-prox` as separate repo and BRAIN index to avoid portfolio duplication.
```
