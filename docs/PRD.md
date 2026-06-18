# **Product Requirements Document (PRD)**
## **Project:** estate-mapper  
**Owner:** Senior Product Lead – Axentx  
**Date:** 2026‑06‑18  
**Version:** 1.0  

---

## 1. Problem Statement
Enterprises with large, heterogeneous IT estates (on‑prem, private cloud, public cloud, legacy VMs, containers, and SaaS services) struggle to:

1. **Discover** all compute resources across disparate environments without manual inventory.  
2. **Understand** actual usage patterns (CPU, memory, network, storage) versus provisioned capacity.  
3. **Identify** the business owners or responsible teams for each asset from fragmented authentication, ticketing, and telemetry logs.  
4. **Prioritize** safe de‑commissioning or migration actions while quantifying risk (e.g., hidden dependencies, compliance constraints).

Current approaches are manual, error‑prone, and siloed, leading to:
- Over‑provisioned resources → $10‑30 M annual waste per 10k VMs (industry average).  
- Unplanned outages during migrations due to unknown dependencies.  
- Inability to present a data‑driven business case for estate rationalization.

**Estate‑mapper** will close this gap by delivering an autonomous agent that continuously maps the full estate, infers usage, attributes ownership, and outputs a ranked list of “safe‑to‑decommission” vs. “high‑risk‑migration” candidates.

---

## 2. Target Users & Personas
| Persona | Role | Pain Points | How estate‑mapper helps |
|---------|------|-------------|--------------------------|
| **Infrastructure Ops Manager** | Oversees data‑center & cloud capacity | Lack of visibility, manual inventory, cost overruns | Automated, up‑to‑date asset map; cost‑saving recommendations |
| **Cloud Migration Lead** | Plans lift‑and‑shift projects | Unknown dependencies, risk of breaking services | Dependency inference & risk ranking for migration sequencing |
| **Security & Compliance Analyst** | Ensures audit readiness | Hidden assets, undocumented owners | Clear ownership attribution, audit‑ready reports |
| **Finance / CFO Office** | Controls IT spend | No justification for de‑commissioning | Quantified waste reduction & ROI calculations |
| **Application Owner / Team Lead** | Owns specific services | Unclear which VMs belong to their apps | Ownership mapping from auth/telemetry logs |

---

## 3. Goals & Success Metrics
| Goal | Success Metric | Target (12 mo) |
|------|----------------|----------------|
| **Automated discovery** | % of total estate assets discovered (vs. manual inventory) | ≥ 95 % |
| **Accurate usage inference** | Correlation between inferred usage and ground‑truth (sampled) | ≥ 90 % |
| **Ownership attribution** | % of assets with confident owner tag (confidence ≥ 0.8) | ≥ 85 % |
| **Risk‑ranked de‑commission list** | Reduction in “unknown‑risk” assets | ≥ 80 % of listed assets have risk ≤ 0.3 |
| **Business impact** | Annual cost savings from de‑commissioned resources | $5 M (baseline 10k VMs) |
| **Adoption** | Number of active enterprise customers using estate‑mapper | 12 paying customers |
| **Reliability** | System uptime / data freshness | 99.5 % uptime, nightly refresh |

---

## 4. Scope

### 4.1 In‑Scope (Must‑Have)
1. **Discovery Engine**  
   - Connectors for major platforms: VMware vSphere, Microsoft Hyper‑V, OpenStack, AWS EC2, Azure VMs, GCP Compute, Kubernetes clusters, and on‑prem bare‑metal via IPMI/Redfish.  
   - Incremental scanning (delta detection) to keep data fresh ≤ 24 h.

2. **Telemetry Ingestion**  
   - Pull usage metrics (CPU, memory, network, storage I/O) from vCenter, CloudWatch, Azure Monitor, Prometheus, and Syslog/Netflow feeds.  
   - Normalise to a common schema.

3. **Auth & Ticket Log Correlation**  
   - Parse AD/LDAP, SSO, IAM logs, and ticketing system (Jira, ServiceNow) to map user/service accounts to assets.  
   - Apply probabilistic ownership model (Bayesian inference) with confidence scoring.

4. **Dependency & Risk Engine**  
   - Build a directed graph of network flows, shared storage, and API calls (using Netflow, sFlow, and service mesh telemetry).  
   - Compute migration risk score (0‑1) based on: external dependencies, compliance tags, SLA criticality, and change‑history frequency.

5. **Output & UI**  
   - REST API delivering JSON payloads: asset list, usage stats, owner, risk score, de‑commission recommendation.  
   - Simple web dashboard (React) with sortable tables, heat‑maps, and export to CSV/Excel.

6. **Security & Governance**  
   - Role‑based access control (RBAC) integrated with corporate IdP (SAML/OIDC).  
   - Data encryption at rest (AES‑256) and in‑flight (TLS 1.3).  
   - Audit log of all queries and actions.

### 4.2 Out‑of‑Scope (Will Not Be Delivered in v1)
- Automated execution of de‑commission actions (only recommendations).  
- Deep application‑level dependency mapping (e.g., database query tracing).  
- Real‑time streaming analytics (batch nightly refresh only).  
- Support for niche hyper‑visors (e.g., Xen, KVM without libvirt).  
- Multi‑tenant SaaS hosting model (initial release is on‑prem/hosted‑by‑customer).  

---

## 5. Key Features (Prioritized)

| Priority | Feature | Description | Acceptance Criteria |
|----------|---------|-------------|---------------------|
| **P1** | **Multi‑Env Discovery Connectors** | Auto‑detect and inventory VMs/containers across supported platforms. | • All connectors return ≥ 95 % of assets compared to manual inventory.<br>• Scans complete within 2 h for 10k assets. |
| **P1** | **Unified Usage Normalisation** | Consolidate CPU, memory, network, storage metrics into a common model. | • Metric granularity ≤ 5 min.<br>• Correlation with source system > 0.9 (Pearson). |
| **P1** | **Ownership Inference Engine** | Probabilistic mapping of assets to owners using auth & ticket logs. | • Confidence ≥ 0.8 for ≥ 85 % of assets.<br>• Manual validation sample error < 5 %. |
| **P2** | **Risk Scoring Graph** | Build dependency graph and compute migration‑risk score. | • Risk score reproducible across runs.<br>• Top‑10 high‑risk assets match expert review. |
| **P2** | **Recommendation Ranking** | Produce ordered list: “Safe‑to‑Decommission” → “Low‑Risk Migration” → “High‑Risk”. | • List updates nightly.<br>• Exportable CSV with all fields. |
| **P3** | **Web Dashboard** | Interactive UI for browsing assets, filters, heat‑maps, and drill‑down. | • UI loads < 3 s for 10k assets.<br>• Filters work on all columns. |
| **P3** | **REST API** | Programmatic access to discovery data and recommendations. | • OpenAPI spec v1.0.<br>• 200 ms median latency for list endpoint. |
| **P4** | **RBAC & Auditing** | Secure access control and immutable audit trail. | • Integration test with SAML IdP passes.<br>• Audit log tamper‑proof. |
| **P4** | **Export & Integration Hooks** | Connectors for PowerBI, ServiceNow CMDB, and custom webhooks. | • Sample PowerBI report refreshes automatically.<br>• Webhook payload matches API spec. |

---

## 6. User Journey (High‑Level Flow)

1. **Onboarding** – Admin provides credentials/API keys for each target environment.  
2. **Initial Scan** – Estate‑mapper runs discovery across all connectors (≈ 2 h).  
3. **Data Normalisation** – Usage, auth, and network logs are ingested and stored in the central PGVector store.  
4. **Inference** – Ownership and risk models run nightly, updating confidence scores.  
5. **Review** – Ops manager logs into dashboard, filters by risk, and exports a de‑commission plan.  
6. **Action** – Team uses exported list to schedule manual shutdowns or migration tickets.  
7. **Feedback Loop** – After each action, user marks outcome (success/failure); model retrains to improve future scores.

---

## 7. Technical Architecture (Brief)

- **Data Ingestion Layer** – Python micro‑services (FastAPI) using async connectors; schedule via Celery + Redis.  
- **Storage** – PostgreSQL for relational metadata + PGVector extension for embedding‑based similarity (owner inference).  
- **Processing** – Spark‑style batch jobs (PySpark) for usage aggregation; custom Bayesian network for ownership; graph‑analytics via Neo4j embedded.  
- **API & UI** – FastAPI backend, React + Ant Design frontend, served via Nginx.  
- **Security** – OAuth2/OIDC, Vault for secret management, audit logging via Elastic Stack.  

---

## 8. Milestones & Timeline

| Milestone | Duration | Deliverable |
|-----------|----------|-------------|
| **M1 – Foundations** | Weeks 1‑4 | Repo scaffold, CI/CD pipeline, basic connector framework |
| **M2 – Discovery Connectors** | Weeks 5‑10 | vSphere, AWS, Azure, K8s connectors (full‑scan) |
| **M3 – Telemetry & Normalisation** | Weeks 11‑14 | Unified usage schema, nightly batch pipeline |
| **M4 – Ownership Engine** | Weeks 15‑20 | Auth log parsers, Bayesian model, confidence API |
| **M5 – Risk Graph** | Weeks 21‑26 | Dependency graph builder, risk scoring algorithm |
| **M6 – API & Dashboard** | Weeks 27‑32 | OpenAPI spec, React UI, export features |
| **M7 – Security & Auditing** | Weeks 33‑36 | RBAC integration, audit log, encryption |
| **M8 – Beta Release & Validation** | Weeks 37‑44 | Pilot with 2 enterprise customers, collect feedback |
| **M9 – GA Launch** | Weeks 45‑48 | Documentation, pricing model, sales enablement |

---

## 9. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Connector brittleness** – API changes in cloud providers break scans. | High (loss of discovery) | Abstract connector layer, automated contract tests, versioned SDKs. |
| **Data privacy** – Sensitive auth logs may be exposed. | High (compliance) | End‑to‑end encryption, on‑prem deployment option, data‑masking for PII. |
| **Model mis‑attribution** – Wrong owner leads to conflict. | Medium | Confidence threshold gating; UI requires manual verification for low‑confidence assets. |
| **Performance at scale** – 100k+ assets cause latency. | Medium | Horizontal scaling of ingestion workers; incremental delta scans; caching of graph calculations. |
| **Customer adoption** – Perceived complexity. | Medium | Provide out‑of‑the‑box templates, guided onboarding wizard, professional services. |

---

## 10. Open Questions

1. Should we support SaaS‑only discovery (e.g., Office 365, Salesforce) in v1 or defer to v2?  
2. What pricing model (subscription per‑asset, per‑environment, or flat‑fee) aligns best with target market?  
3. Will we need a separate “Compliance” module for GDPR/PCI tagging?  

*Answers to be resolved in the next product review (Week 6).*

--- 

**Prepared by:**  
Senior Product Lead – Axentx  
[arkashira/surrogate-1-harvest]  

*Document status: Draft – review required by Architecture, Engineering, and Sales leads.*
