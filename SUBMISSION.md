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

The green [GitHub Actions workflow](https://github.com/Ifem1/qualisort/actions/workflows/ci.yml) passed all 44 direct tests, all 9 unit tests, both AST lint checks, and semantic validation plus schema extraction for both contracts. On the Windows workspace, the latter two checks are blocked by access denied in the local linter cache. QualiSort is finalized on Studionet at [`0xE63Bb511028D61A9e109A5B96E344b6b47B18C33`](https://explorer-studio.genlayer.com/address/0xE63Bb511028D61A9e109A5B96E344b6b47B18C33); the second-IC consumer proof is also finalized. See [`docs/LIVE_EVIDENCE.md`](docs/LIVE_EVIDENCE.md) for transaction-level evidence and the precise verification boundary.

The prior deployment is superseded by corrected QualiSort address [`0xc6e4D96274137f4b0C432e9b42E0a1D80C20D872`](https://explorer-studio.genlayer.com/address/0xc6e4D96274137f4b0C432e9b42E0a1D80C20D872), finalized in transaction [`0xfc05b5353d2a10ed229183ca7ea0161df2610d22dd894b49c25d927194a0f48c`](https://explorer-studio.genlayer.com/tx/0xfc05b5353d2a10ed229183ca7ea0161df2610d22dd894b49c25d927194a0f48c). A new lifecycle against this address was not claimed without observed pool/seal/draw receipts.
