# ROADMAP.md – estate‑mapper

**Product Vision**  
An autonomous agent that continuously discovers virtual machines and services across heterogeneous, legacy data‑center estates, infers real‑time usage and ownership from network, telemetry, and authentication logs, and outputs a ranked list of safe‑to‑decommission or migration‑risk assets.  

**Target Market** – Large enterprises and managed service providers that must reduce cloud‑sprawl, cut licensing costs, and meet compliance/green‑IT mandates.

---

## MVP (Must‑Have for Launch) – **🚀 Release 0.1**

| Feature | Description | Acceptance Criteria | Owner |
|---------|-------------|----------------------|-------|
| **Auto‑Discovery Engine** | Periodic scan of hypervisors, containers, and on‑prem services (vSphere, Hyper‑V, KVM, Docker, Kubernetes). | • Detect ≥ 95 % of assets in a test estate (≥ 5 k VMs).<br>• Runs on a configurable schedule (default 24 h). | Infra Lead |
| **Telemetry & Auth Log Ingestion** | Connectors for syslog, Windows Event Log, and cloud‑native logs (AWS CloudTrail, Azure Activity). | • Ingest ≥ 10 M log events/day without loss.<br>• Normalised schema stored in PostgreSQL + TimescaleDB. | Data Engineer |
| **Usage Inference Model** | Lightweight statistical model (baseline + anomaly detection) that maps CPU, network, storage metrics to “active”, “idle”, or “unknown”. | • ≥ 90 % precision on labeled test set (internal dataset).<br>• Model runs < 5 s per 10 k assets. | ML Engineer |
| **Ownership Attribution** | Correlate auth events (logins, SSH keys, service accounts) to assets and produce a ranked owner list. | • Top‑3 owners correct for ≥ 85 % of assets (validated against CMDB). | Backend Lead |
| **Risk Scoring & Ranking** | Combine usage & ownership signals into a “decommission risk” score (0‑100) and produce a sorted export (CSV/JSON). | • Score distribution matches manual audit (R² > 0.8). | Product Lead |
| **Dashboard (MVP UI)** | Simple web UI (React + Flask) showing: total assets, usage breakdown, top‑ranked decommission candidates, and drill‑down per asset. | • Auth via SSO (SAML/OIDC).<br>• UI loads < 2 s for 5 k assets. | Front‑end Lead |
| **CI/CD & Observability** | GitHub Actions pipeline, unit/integration tests (≥ 80 % coverage), Prometheus metrics, Loki logs. | • Deployable with a single `helm install estate-mapper`. | DevOps |
| **Documentation & Quick‑Start** | README, installation guide, API spec (OpenAPI 3.0). | • New user can spin up a demo environment in ≤ 30 min. | Technical Writer |

**MVP Success Metric:** 3 pilot customers adopt the agent and achieve ≥ 15 % reduction in idle VM spend within 60 days.

---

## Post‑MVP Roadmap

### Phase 1 – **v1.0 – Enterprise‑Ready Enhancements** (Quarter 2 2027)

| Theme | Key Initiatives |
|-------|-----------------|
| **Scalable Discovery** | • Add support for VMware NSX, OpenStack, and legacy bare‑metal inventory tools.<br>• Parallelised scanning with vLLM‑style async workers for > 50 k assets. |
| **Advanced Usage Modeling** | • Replace baseline model with a fine‑tuned transformer (leveraging `vLLM` inference) for workload classification (web, DB, batch, AI).<br>• Auto‑retrain nightly on new telemetry. |
| **Ownership Confidence Scores** | • Fuse IAM data (Azure AD, Okta, LDAP) and code‑repo ownership (Git history) into Bayesian confidence metric.<br>• Provide “owner‑verification” UI flow. |
| **Policy Engine** | • Define decommission policies (e.g., “idle > 30 days & cost < $5/mo”).<br>• Export actionable tickets to ServiceNow, Jira, or custom webhook. |
| **Security & Compliance** | • Role‑based access control (RBAC) for UI & API.<br>• GDPR‑compliant data retention & audit logs. |
| **Performance & Reliability** | • Horizontal scaling via Kubernetes Operator.<br>• SLA: 99.5 % uptime, < 2 min latency for risk‑score queries. |
| **Customer Success Kit** | • On‑boarding wizard, best‑practice playbooks, and ROI calculator. |

**v1.0 Launch Metric:** 10 paying customers, average ROI ≥ 20 % cost savings, NPS ≥ 45.

---

### Phase 2 – **v2.0 – Automation & Ecosystem Integration** (Quarter 4 2027)

| Theme | Key Initiatives |
|-------|-----------------|
| **Closed‑Loop Decommission Automation** | • Integrate with cloud provider APIs (AWS, Azure, GCP) to schedule stop/terminate actions after human approval.<br>• Automated snapshot & backup before termination. |
| **Predictive Migration Planning** | • Forecast future capacity needs using time‑series models (TimescaleDB + Prophet).<br>• Recommend target environments (e.g., move to spot instances, containers). |
| **Marketplace Connectors** | • Pre‑built adapters for ServiceNow CMDB, Splunk, Elastic, and HashiCorp Terraform.<br>• Publish a public SDK for third‑party extensions. |
| **AI‑Assisted Insight Assistant** | • Deploy an LLM‑powered chat assistant (via `SGLang`) that can answer “Why is VM‑X flagged?” or “What would be the impact of decommissioning service‑Y?”. |
| **Multi‑Tenant SaaS Offering** | • Refactor to support isolated tenant data stores, billing metering, and self‑service provisioning.<br>• Introduce usage‑based pricing tiers. |
| **Compliance Reporting** | • Generate PCI/DSS, ISO, and internal audit reports automatically from risk scores and actions taken. |
| **Global Deployments** | • Support edge‑region agents with low‑bandwidth log shipping (gRPC + protobuf). |

**v2.0 Launch Metric:** 30+ SaaS tenants, 40 % of decommission actions fully automated, churn < 5 %.

---

## Ongoing Maintenance & Improvement

| Activity | Frequency |
|----------|-----------|
| **Model Retraining & Evaluation** | Weekly (auto) + quarterly manual review |
| **Security Patch Cycle** | Immediate on CVE, otherwise monthly |
| **Customer Feedback Loop** | Bi‑weekly sprint demos, quarterly NPS analysis |
| **Data Quality Audits** | Monthly sampling of log ingestion & ownership mapping |
| **Performance Benchmarking** | Quarterly load‑test against 100 k asset estates |

---

## Release Cadence

- **Sprint Length:** 2 weeks (scrum)
- **Release Frequency:** MVP – one‑off; v1.0 – every 4 weeks; v2.0 – every 6 weeks (feature‑flagged)
- **Hotfixes:** As needed, within 24 h for critical bugs.

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Log volume overload | Service degradation | Back‑pressure queue + scalable Kafka ingestion |
| Ownership data privacy | Legal/compliance | Data‑masking, consent‑based collection, audit trails |
| Model drift | Incorrect risk scores | Continuous monitoring, auto‑retrain thresholds |
| Integration complexity | Slower adoption | Provide certified connector templates & sandbox env |

---

*Prepared by the Estate‑Mapper Product & Engineering Leadership Team – June 2026*
