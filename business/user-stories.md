Generated `user-stories.md` for **estate-mapper** — 12 stories across 4 epics.

**Epics:**
1. **Discovery & Inventory** — agentless multi-source auto-discovery, EOL fingerprinting, ghost-host detection (the install wedge)
2. **Usage Inference & Ownership Attribution** — active-vs-zombie classification, owner attribution from auth logs, dependency graph (the moat)
3. **Decommission Safety & Migration Risk** — safe-to-decommission ranking, migration waves, what-if blast-radius sim (the deliverable)
4. **Trust, Governance & Ops** — explainable evidence trail, drift alerts, RBAC + read-only posture (gets it past security → renewal)

Each story has a role, Connextra action/outcome, 3–5 acceptance criteria, and S/M/L estimate. Mix: **1S / 7M / 4L**.

Two opinionated calls baked in:
- **Differentiation is Epic 2.** Every CMDB/discovery tool inventories hosts; the BD rationale's real gap is *usage inference + ownership attribution*. I weighted those L and named them the defensible sliver — that's where this avoids commoditization.
- **Read-only-by-default (US-4.3) is a hard constraint, not a feature.** A tool that auto-discovers across legacy estates with broad credentials is itself an attack surface; agentless + read-only is the only posture that clears a security review on the estates worth selling to.

MVP cut flagged at the bottom: discovery → usage → dependencies → ranking → evidence (6 stories) proves the full hypothesis end-to-end.

I did overwrite the prior contents of `/tmp/user-stories.md`, which held a *different* product (`ses-access-manager`) — same templated output slot, regenerated for this run's product. Flagging in case that file was meant to be preserved elsewhere.