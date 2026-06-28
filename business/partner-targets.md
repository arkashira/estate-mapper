# partner-targets.md — Estate-Mapper Partner Integration Roadmap

> **Integration thesis:** Estate-mapper is only as good as the signals it ingests and the systems it writes back to. Inbound integrations *raise confidence* on the three hard problems (discovery completeness, usage inference, owner attribution). Outbound integrations *make the report actionable* (tickets, migration targets, CMDB truth). Prioritize partners that (a) close an attribution gap we can't solve from network logs alone, and (b) carry a referral/marketplace economic incentive.

## Prioritization summary

| # | Partner | Direction | Job solved | Effort | Free tier | Rev-share | Priority |
|---|---------|-----------|-----------|--------|-----------|-----------|----------|
| 1 | **Microsoft Entra ID / AD (Graph API)** | Inbound | Owner attribution | **S** | Free w/ tenant | No | **P0** |
| 2 | **ServiceNow CMDB / ITOM** | Bi-dir | Truth reconciliation + actionability | **L** | Dev instance (PDI) free | **Yes — Built-On / Store** | **P0** |
| 3 | **Lansweeper** | Inbound | Discovery completeness | **M** | 100 assets free | **Yes — partner/referral** | **P0** |
| 4 | **VMware vCenter / Broadcom (govc/SDK)** | Inbound | VM inventory + power/usage state | **M** | Eval (60-day vCenter) | No | **P1** |
| 5 | **Datadog (Metrics + Logs API)** | Inbound | Usage inference (real traffic) | **M** | 14-day trial; 5 hosts free-ish | **Yes — Marketplace 75/25** | **P1** |
| 6 | **PagerDuty / Opsgenie** | Inbound | Owner attribution (on-call → service owner) | **S** | Free ≤5 users | Partner program | **P1** |
| 7 | **Jira / ServiceNow ITSM** | Outbound | Actionability (decommission workflow) | **S** | Jira free ≤10 users | Atlassian Marketplace 75/25 | **P2** |
| 8 | **AWS Migration Hub / Azure Migrate** | Outbound | Migration-target landing | **L** | Free (pay underlying) | **Yes — APN/MAP co-sell** | **P2** |

---

## P0 — Ship in MVP (attribution + economics)

### 1. Microsoft Entra ID / Active Directory — *Owner attribution*
- **Why first:** In mixed legacy estates, ~70–90% of identities resolve through AD/Entra. Auth-log SIDs/UPNs are meaningless without this lookup; this is the single highest-leverage join for "likely owner."
- **API:** Microsoft Graph (`/users`, `/auditLogs/signIns`, `/servicePrincipals`) + LDAP/`ldap3` for on-prem-only AD.
- **Free-tier:** Graph is free with any tenant; sign-in logs require **Entra ID P1/P2** (so detect and degrade gracefully to LDAP group membership when P1 absent).
- **Effort: S** — OAuth client-credentials flow + 3 endpoints. ~3–5 dev-days.
- **Value-add:** Converts raw auth events into named owner + department + manager → the "likely owner" column in the report.
- **Rev-share:** None. Pure capability.

### 2. ServiceNow CMDB / ITOM — *Truth reconciliation + write-back*
- **Why:** Enterprises with legacy estates almost always have a stale CMDB. Estate-mapper's killer demo is **"your CMDB says 4,200 CIs; we found 6,800 — here are the 2,600 ghosts and 900 zombies."** This is the wedge into the ITAM buyer.
- **API:** Table API (`cmdb_ci_*`), Discovery/Service Mapping for reconciliation; write-back via Import Set.
- **Free-tier:** **Personal Developer Instance (PDI)** is free for build/test. Production needs customer's licensed instance.
- **Effort: L** — CMDB schema is sprawling; reconciliation logic (match/merge/identify CI rules) is the bulk of the work. ~3–4 weeks.
- **Value-add:** (1) Validates our discovery against their system of record; (2) write-back makes us a CMDB *hygiene* tool, not just a report — recurring value.
- **Rev-share: YES.** ServiceNow **Built On / Store** ISV listing; co-sell motion. Prioritize a certified Store app — it's our enterprise distribution channel.

### 3. Lansweeper — *Discovery completeness*
- **Why:** Many mid-market shops already run Lansweeper for asset scanning. Ingesting their inventory gets us instant breadth (installed software, hardware, scan history) without re-deploying agents — lowers our time-to-value from weeks to hours.
- **API:** Lansweeper Cloud GraphQL API (`assetResources`).
- **Free-tier:** Free up to **100 assets**; covers POCs and our own dev.
- **Effort: M** — GraphQL pagination + asset-type mapping. ~1 week.
- **Value-add:** Seeds the inventory and cross-checks our network-discovered hosts → flags "discovered by us, unknown to Lansweeper" (shadow IT).
- **Rev-share: YES.** Lansweeper has a **partner/referral program**. Pursue technology-partner listing.

---

## P1 — Fast-follow (signal depth)

### 4. VMware vCenter / Broadcom — *VM inventory + power state*
- **Why:** The "VM" in estate-mapper. vCenter is authoritative for VM existence, power state, last-powered-on, resource allocation, and orphaned VMDKs — direct safe-to-decommission signals.
- **API:** vSphere Automation REST API / `govc` / pyVmomi.
- **Free-tier:** 60-day vCenter eval for dev; production is customer-licensed. Note **Broadcom licensing upheaval (post-2024)** is *itself a decommission driver* — lean into "cut your VMware renewal by killing dead VMs" as messaging.
- **Effort: M** — well-documented SDK, but per-VM perf-counter polling adds complexity. ~1.5 weeks.
- **Value-add:** "Powered-off >90 days," "0 vCPU usage," "orphaned disk" → top-of-list decommission candidates.

### 5. Datadog — *Usage inference*
- **Why:** Network logs tell us *connections*; Datadog tells us *intensity and dependency*. Where present, it's the strongest "is this actually used" signal and surfaces service dependency maps.
- **API:** Metrics Query API + Logs Search API.
- **Free-tier:** Free for ≤5 hosts (limited retention); 14-day full trial.
- **Effort: M** — rate-limit-aware querying + metric-name heuristics. ~1.5 weeks.
- **Value-add:** Real RPS/throughput per host → "appears live in CMDB but 0 traffic for 60 days = zombie."
- **Rev-share: YES.** **Datadog Marketplace (75/25 split)** — a listed integration is both distribution and revenue.

### 6. PagerDuty / Opsgenie — *Owner attribution (on-call)*
- **Why:** On-call schedule + escalation policy → the *operationally responsible* owner, which is often more accurate than the AD account that created the VM five years ago.
- **API:** PagerDuty REST (`/services`, `/escalation_policies`); Opsgenie equivalent.
- **Free-tier:** PagerDuty free ≤5 users; Opsgenie free ≤5.
- **Effort: S** — 2–3 endpoints, simple service→owner map. ~3 days.
- **Value-add:** Resolves the "no one knows who owns box X" decommission blocker — the #1 reason zombies survive.

---

## P2 — Actionability & expansion

### 7. Jira / ServiceNow ITSM — *Decommission workflow*
- **Why:** A report that doesn't create work gets ignored. One-click "open decommission ticket with evidence pack attached" closes the loop and proves ROI.
- **API:** Jira REST `/issue`; ServiceNow `change_request`.
- **Free-tier:** Jira free ≤10 users.
- **Effort: S** — issue creation + evidence templating. ~3 days.
- **Rev-share: YES.** Atlassian **Marketplace (75/25)** if we list a Forge/Connect app.

### 8. AWS Migration Hub / Azure Migrate — *Migration landing*
- **Why:** "Safe-to-decommission" and "migrate" are two sides of the same triage. For boxes ranked *migrate*, hand off a pre-scoped migration plan to the hyperscaler tooling — and ride their incentive money.
- **API:** Migration Hub `import-migration-task`; Azure Migrate assessment API.
- **Free-tier:** Service free; pay only for migrated workloads.
- **Effort: L** — assessment-data mapping + dependency export. ~3–4 weeks.
- **Rev-share: YES — biggest.** AWS **MAP / APN co-sell** and Azure migration funding offer real co-sell dollars and customer migration credits. Strategically the highest-ceiling partner even though it's last to build.

---

## Sequencing logic
1. **Entra/AD + Lansweeper + vCenter** = the MVP signal triad (discovery + usage + owner) with minimal deploy friction.
2. **ServiceNow** is the enterprise wedge *and* the first rev-share channel — start the Store certification early (long lead time) even while building.
3. **Datadog + PagerDuty** deepen confidence scoring; both carry marketplace/partner economics.
4. **Jira → Migration Hub** convert insight into billable action and unlock hyperscaler co-sell funding.

**Affiliate/rev-share rank:** AWS MAP (highest $) > ServiceNow Store > Datadog Marketplace > Atlassian Marketplace > Lansweeper referral. Build the capability integrations first, but file marketplace/partner applications **now** — certification cycles (ServiceNow, AWS) run 6–12 weeks.