Generated `dataflow.md` at `/tmp/estate-mapper/dataflow.md`.

Key opinionated calls baked in:

- **Agentless, read-only, outbound-mTLS-only collector** (Auth Boundary A) — the single biggest unlock for selling into nervous 10–15yr legacy estates. No inbound ports, no prod agents.
- **Three explicit auth boundaries** — A: collector→SaaS (pinned mTLS), B: storage tenant isolation (PG RLS + per-tenant KMS), C: serving (OIDC/SAML SSO + RBAC + per-record audit).
- **Evidence-carrying graph, not a black box** — every correlation edge, ownership candidate, and risk score ships with provenance. The buying moment is a change-advisory-board review, so scores have to be *defensible*, not just produced.
- **pgvector/BRAIN tie-in** — cross-engagement learning on prior decommission outcomes, consistent with the shared company brain.

The diagram splits the customer trust zone from our SaaS trust zone at the collector boundary, which is where the actual security risk and sales objection live.