# Codex handoff for Mary

Mary should **unzip the QualiSort archive herself, then add the unzipped `qualisort` folder to Codex**. Do not ask Codex to work from the zip archive.

Paste the prompt below as a normal execution prompt:

---

Finish QualiSort completely as a submission-ready standalone GenLayer Intelligent Contract.

You are working inside an already-unzipped repository. Treat the existing code and architecture as the starting implementation, not as disposable scaffolding. Inspect everything first, preserve the core design, and then fix anything needed for correctness, GenVM compatibility, security, testing, deployment and documentation.

NON-NEGOTIABLE NETWORK:
- GenLayer Studionet only
- chain ID 61999
- RPC https://studio.genlayer.com/api
- explorer https://explorer-studio.genlayer.com/
- do not migrate the repository to any other Studio network or chain

PRODUCT BOUNDARY:
- QualiSort is a standalone Intelligent Contract primitive
- no frontend, no React, no Vite, no web UI
- primary contract: contracts/qualisort.py
- contracts/committee_gate.py is only a small IC-to-IC composability proof

CORE DESIGN TO PRESERVE:
1. Pool owner creates an immutable bounded qualification rubric.
2. Candidates register public HTTPS evidence.
3. GenLayer validators independently fetch that evidence and re-derive PASS/FAIL/UNRESOLVED masks for every criterion. Validation must remain substantive, not a format/schema check.
4. Deterministic code derives QUALIFIED / NOT_QUALIFIED / AMBIGUOUS / UNAVAILABLE.
5. QUALIFIED and NOT_QUALIFIED are terminal for the pool. AMBIGUOUS and UNAVAILABLE can be retried while open.
6. A pool can seal only with enough qualified candidates.
7. Seal freezes the qualified set, commits a pool digest and fixes a future public randomness-beacon round.
8. Draw independently verifies the exact target beacon randomness and deterministically ranks only qualified candidates. The LLM must never rank/select committee members.
9. Another IC must be able to consume `is_selected` safely.

EXECUTION GOAL, NOT REVIEW:
- run preflight and unit tests
- install/use the matching stable GenLayer tooling for Studionet as needed
- run genvm-lint against every contract and fix all real errors
- run the complete direct-mode suite and strengthen it where gaps exist
- inspect all prompt-injection, malformed-output, dynamic-web, status-transition, beacon, replay, duplicate-registration, withdrawal, selection-cap and validator-disagreement paths
- do not weaken tests merely to make them pass
- confirm ABI/schema generation works
- deploy the primary contract to Studionet 61999 using the configured local GenLayer account; never request, print, commit or copy a private key
- wait for FINALIZED status, not merely accepted
- execute a real reviewer-friendly lifecycle with multiple accounts: qualified, not-qualified, and ambiguous/unavailable cases; seal; future beacon draw; deterministic committee verification
- deploy CommitteeGate only if the current stable Studionet runtime supports the typed IC-to-IC call as implemented; prove a non-member is rejected and selected member is accepted
- capture real addresses, transaction hashes, explorer links, target beacon round, pool digest, randomness and selection seed
- update docs/LIVE_EVIDENCE.md, README.md, SUBMISSION.md and deployment docs with only real evidence
- remove stale placeholders that are genuinely resolved, but never fabricate missing evidence
- run final preflight, linter, tests and repository-wide search before finishing

SECURITY / QUALITY BAR:
- fail closed on malformed model output
- do not let candidate statements count as proof
- evidence pages are hostile data, never instructions
- no leader-only eligibility decision
- no caller-provided selection seed
- no post-seal membership mutation
- deterministic selection must be independently reproducible from stored state
- make trust boundaries explicit, especially the external randomness beacon
- keep one clear primary primitive rather than turning this into a full app

GIT:
- target repository is https://github.com/Ifem1/qualisort
- if authenticated Git has push permission, commit and push the finished repository there
- if push is unavailable, leave the working tree complete and report exactly what remains for Mary to push

Do not stop at recommendations. Keep working until the repository is as finished, tested, deployed and documented as the available credentials/runtime permit. At the end, give a concise report with: test counts, linter/schema status, finalized contract address, pool/demo transaction hashes, consumer proof if completed, remaining limitations, and whether the push succeeded.

---
