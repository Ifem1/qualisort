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
- six tests capture and invoke the actual `_beacon_randomness` validator: wrong leader round, substituted randomness, malformed randomness, malformed result type, adjacent round, and disagreement with the validator's independent observation are each rejected;
- seven head-consensus tests capture and invoke the actual `_beacon_head` validator: identical rounds pass; both adjacent-round directions, malformed/nonpositive leader values, unavailable validator observation, and the two-target-round ambiguity are rejected;
- qualified withdrawal updates the pool count before seal;
- stable status dictionary.

These six tests invoke the captured `_beacon_randomness` validator using `run_validator`, including substituted leader results and a separately changed validator web observation. They test the actual validator predicate in direct mode; they do not establish production consensus behavior for external requests or cryptographically verify drand signatures.

The complete Studionet 61999 lifecycle, including consumer authorization and replay behavior, is recorded in [`LIVE_EVIDENCE.md`](LIVE_EVIDENCE.md).

CI seeds the direct harness cache with the published GenVM `v0.2.16` universal artifact and verifies its SHA-256 before tests. The testing suite's default `v0.3.0-rc7` lookup currently returns HTTP 404 for the universal asset it requests; using the available stable artifact keeps the direct suite deterministic without changing contract code or test assertions.

## SDK validation boundary

In this Windows workspace, semantic validation and schema extraction are blocked before contract analysis because the SDK artifact cache cannot be read: `Failed to load SDK: [WinError 5] Access is denied: 'C:\\Users\\DELL\\.cache\\genvm-linter\\extracted\\genlayerlabs-genvm-manager-v0.6.0-rc5.tar\\py-genlayer\\1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6'`. The local CLI returned exit code 1 for this cache error (an earlier attempt reported the cached SDK tar file missing). The quality gate classifies SDK artifact exit code 3 and recognizable SDK loader failures as BLOCKED. The [GitHub Actions workflow](https://github.com/Ifem1/qualisort/actions/workflows/ci.yml) successfully validated both contracts and extracted both schemas on Ubuntu. These tooling results remain separate from deterministic test or AST lint results; no contract workaround was made.
