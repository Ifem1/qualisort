# Test plan

The direct-mode suite is designed around protocol invariants rather than line coverage.

Covered cases include:

- canonical bounded rubric creation;
- malformed/duplicate criteria rejection;
- HTTPS/public-host evidence gate;
- one registration per address per pool;
- required criteria pass -> QUALIFIED;
- required criterion fail -> NOT_QUALIFIED;
- required unresolved -> AMBIGUOUS;
- unavailable evidence -> UNAVAILABLE;
- malformed/overlapping model masks fail closed;
- terminal assessments cannot be re-run to cherry-pick;
- ambiguous/unavailable outcomes can be retried while open;
- only the owner can seal;
- insufficient qualified population cannot seal;
- seal fixes a future beacon round and pool digest;
- exact target-round beacon drives deterministic selection;
- validator independently re-derives qualification rather than checking output shape;
- a substituted malicious leader proposal is rejected by the validator predicate;
- qualified withdrawal updates the pool count before seal;
- stable status dictionary.

The installed direct-mode harness does not preserve malformed drand response payloads consistently across the unsafe validator boundary. Wrong-round and validator disagreement cases must be verified against the validator predicate with explicit substituted results and in a real consensus deployment; the direct-mode mock test does not establish a live beacon guarantee.

The complete Studionet 61999 lifecycle, including consumer authorization and replay behavior, is recorded in [`LIVE_EVIDENCE.md`](LIVE_EVIDENCE.md). This live run does not replace isolated wrong-round and validator-disagreement tests listed above.
