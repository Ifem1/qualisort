# QualiSort submission notes

## Category

Standalone GenLayer Intelligent Contract.

No frontend. No product UI. The reusable primitive is `contracts/qualisort.py`.

## Primitive

QualiSort separates committee formation into two trust domains:

- GenLayer consensus decides whether each candidate meets an immutable natural-language rubric from public evidence.
- deterministic future-beacon sortition selects only from the resulting qualified set.

The LLM cannot choose winners, set randomness, alter the rubric, or make an unqualified candidate selectable.

## Consensus logic

Qualification uses a custom validator. Leader and validators independently fetch the same evidence URLs and derive total PASS/FAIL/UNRESOLVED criterion masks. Validators compare the fields that affect qualification, not free-form text.

The exact target randomness-beacon round is also independently re-fetched at draw time. Committee ranking is deterministic hashing after consensus. The IC observes the public drand response through GenLayer consensus; it does not cryptographically verify the beacon threshold signature itself.

## State design

Pools have OPEN -> SEALED -> DRAWN finality. Candidate states distinguish retryable operational uncertainty (`AMBIGUOUS`, `UNAVAILABLE`) from terminal semantic outcomes (`QUALIFIED`, `NOT_QUALIFIED`). Seal commits the policy and frozen qualified population into `pool_digest`.

## Reuse

Consumer contracts only need `is_selected`, `is_qualified`, or `get_committee`. `contracts/committee_gate.py` is a minimal companion consumer.

## Network

Studionet only: chain 61999, `https://studio.genlayer.com/api`.

## Verification and live status

The direct suite has 22 passing checks and the unit suite has 5 passing checks. AST lint passes for both contracts. Semantic SDK validation and schema extraction could not run because the installed linter's SDK cache is incomplete; its retry reported a missing SDK tarball. QualiSort is finalized on Studionet at [`0xE63Bb511028D61A9e109A5B96E344b6b47B18C33`](https://explorer-studio.genlayer.com/address/0xE63Bb511028D61A9e109A5B96E344b6b47B18C33); the second-IC consumer proof is also finalized. See [`docs/LIVE_EVIDENCE.md`](docs/LIVE_EVIDENCE.md) for transaction-level evidence and the precise verification boundary.
