# QualiSort

**Consensus-qualified committee sortition for GenLayer.**

QualiSort creates committees in two deliberately separate stages:

1. **Qualification is semantic.** GenLayer validators independently inspect frozen public evidence against an immutable rubric and agree on which candidates qualify.
2. **Selection is mechanical.** A future public randomness-beacon round, fixed only after the qualified set is sealed, produces a deterministic committee. The LLM never chooses winners.

QualiSort is a standalone Intelligent Contract primitive, not an app. **There is no frontend by design.** The main submission is `contracts/qualisort.py`; `contracts/committee_gate.py` is a tiny optional consumer showing how another IC can gate an action to selected committee members.

## Network

QualiSort is intentionally scoped to **GenLayer Studionet, chain ID 61999**.

- RPC: `https://studio.genlayer.com/api`
- Explorer: `https://explorer-studio.genlayer.com/`
- Contract runtime header: stable `py-genlayer` dependency used by the existing Studionet contract set

No alternate Studio network is part of this repository.

## Why this needs GenLayer

A deterministic smart contract can shuffle addresses, but it cannot reliably decide whether a candidate satisfies a natural-language qualification standard backed by public evidence. A normal AI service can make that judgement, but one service then controls committee eligibility.

QualiSort splits the problem at the correct trust boundary:

```text
public evidence + immutable rubric
              |
              v
independent GenLayer semantic consensus
              |
        QUALIFIED SET
              |
           seal hash
              |
              v
 future public beacon randomness
              |
              v
 deterministic hash ranking
              |
          COMMITTEE
```

The consensus step cannot select a preferred candidate. The sortition step cannot make an unqualified candidate eligible.

## Qualification model

Pool creators provide up to six bounded criteria:

```json
[
  {
    "id": "PYTHON",
    "description": "Has public evidence of production Python engineering.",
    "required": true
  },
  {
    "id": "SECURITY",
    "description": "Has public evidence of security review work.",
    "required": true
  },
  {
    "id": "RECENT",
    "description": "Has relevant public work from the last two years.",
    "required": false
  }
]
```

Each candidate supplies 1–3 HTTPS evidence URLs. Validators independently fetch those URLs and classify every criterion as exactly one of:

- `PASS`
- `FAIL`
- `UNRESOLVED`

The model output is reduced to three disjoint bitmasks. Deterministic contract code then derives the candidate state:

- `QUALIFIED`
- `NOT_QUALIFIED`
- `AMBIGUOUS`
- `UNAVAILABLE`

Required criteria must pass. Optional unresolved criteria can produce `AMBIGUOUS` when they could change whether `min_pass` is reached. `AMBIGUOUS` and `UNAVAILABLE` are retryable while the pool is open; `QUALIFIED` and `NOT_QUALIFIED` are terminal for that pool, reducing outcome cherry-picking.

## Validator design

QualiSort does not ask validators to approve valid JSON. The leader proposes only qualification-affecting fields:

```text
reachable_count
model_valid
pass_mask
fail_mask
unresolved_mask
```

Each validator independently re-fetches the same evidence, re-runs the same bounded rubric judgement, and accepts only if those substantive fields match. Free-form rationale is diagnostic and does not affect eligibility.

The evidence prompt explicitly treats candidate statements and web pages as hostile data. A candidate statement is context, never proof.

## Sortition model

Once enough candidates are qualified, the pool owner seals the set. During sealing, validators independently observe the current public randomness-beacon head and the contract commits to a round five rounds in the future.

That future round is not known when the qualified set is sealed.

When the target round is available, anyone may call `draw_committee`. Validators independently fetch the exact target round and must agree on the published randomness. QualiSort then computes:

```text
pool_digest = H(pool configuration + frozen qualified set + target round)
seed        = H("QualiSort/v1" + pool_digest + target round + beacon randomness)
score_i     = H(seed + candidate_id + candidate address)
```

Qualified candidates are sorted by `score_i`, and the first `committee_size` entries are selected.

The model has no role in that ordering.

## State model

### Pool

```text
OPEN -> SEALED -> DRAWN
     -> CANCELLED
```

An open pool accepts candidates and qualification attempts. A sealed pool freezes eligibility and the future beacon round. A drawn pool has a permanent committee.

### Candidate

```text
REGISTERED
  |-- QUALIFIED        terminal
  |-- NOT_QUALIFIED    terminal
  |-- AMBIGUOUS        retryable while OPEN
  |-- UNAVAILABLE      retryable while OPEN
  `-- WITHDRAWN        terminal
```

## Reuse surface

Consumer contracts do not need to understand the rubric or randomness machinery. They can use:

```python
is_qualified(pool_id, address)
is_selected(pool_id, address)
get_committee(pool_id)
```

`contracts/committee_gate.py` demonstrates a second IC that checks `is_selected()` before accepting an action and prevents action replay.

## Rotation support

`prior_selection_cap` is optional per pool. When non-zero, candidates who have already been selected that many times by QualiSort cannot register. This creates a simple deterministic rotation policy without letting an LLM decide who has served "too often".

## Security boundaries

QualiSort intentionally does **not** claim the following:

- It does not prove real-world identity. It qualifies the submitting address against the frozen public evidence supplied for that pool.
- It does not make the public randomness beacon trustless. Validators agree on the exact public beacon output; they do not verify the beacon's threshold signature inside this contract.
- It does not hide candidates or evidence.
- It does not guarantee a candidate remains qualified forever. Qualification is a snapshot for one sealed pool.
- It does not let the LLM rank or select candidates.

The pool owner controls when to seal an open pool. Once sealed, the eligibility set, pool digest, and future beacon round are frozen.

## Repository layout

```text
contracts/qualisort.py          primary reusable primitive
contracts/committee_gate.py     tiny IC-to-IC consumer example
tests/direct/                   GenLayer direct-mode adversarial tests
tests/unit/                     dependency-free repository checks
scripts/preflight.py            network/source invariant gate
scripts/check_all.py            local quality gate
scripts/deploy_studionet.py     explicit 61999 deployment helper
docs/                           architecture, threats, deployment, live evidence
examples/criteria.json          example bounded rubric
```

## Test locally

Cheap tests require only Python + pytest:

```bash
python scripts/preflight.py
pytest tests/unit -q
```

Full direct-mode tests:

```bash
python -m pip install -r requirements-test.txt
pytest tests/direct -q
```

Full quality gate, when optional tools are installed:

```bash
python scripts/check_all.py
```

The green [GitHub Actions workflow](https://github.com/Ifem1/qualisort/actions/workflows/ci.yml) passed preflight, all 9 unit tests, both AST lint checks, all 44 direct-mode tests, and semantic validation plus schema extraction for both contracts. On this Windows workspace, SDK validation/schema remain locally blocked by access denied in the linter cache; the CI result verifies those checks on Ubuntu. See [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md) for direct-mode coverage and [`docs/LIVE_EVIDENCE.md`](docs/LIVE_EVIDENCE.md) for deployment status.

## Deploy to Studionet

The helper never asks for or stores a private key. Configure and unlock the GenLayer CLI account first, then:

```bash
python scripts/deploy_studionet.py
```

Equivalent direct CLI deployment:

```bash
genlayer deploy --contract contracts/qualisort.py --rpc https://studio.genlayer.com/api
```

The finalized Studionet deployment and end-to-end lifecycle are recorded in [`docs/LIVE_EVIDENCE.md`](docs/LIVE_EVIDENCE.md). The live evidence includes transaction receipts, pool and candidate states, the committed future drand round, stored committee membership, and a consumer-contract authorization and replay proof.

## Finalized Studionet lifecycle

QualiSort’s current canonical deployment is [`0xc6e4D96274137f4b0C432e9b42E0a1D80C20D872`](https://explorer-studio.genlayer.com/address/0xc6e4D96274137f4b0C432e9b42E0a1D80C20D872), finalized in transaction [`0xfc05b5353d2a10ed229183ca7ea0161df2610d22dd894b49c25d927194a0f48c`](https://explorer-studio.genlayer.com/tx/0xfc05b5353d2a10ed229183ca7ea0161df2610d22dd894b49c25d927194a0f48c). Pool 1 completed qualification, sealing at target round 6,486,213, and deterministic committee draw; all receipts and stored randomness are in [`docs/LIVE_EVIDENCE.md`](docs/LIVE_EVIDENCE.md). The corrected deployment requires exact latest-beacon head equality at seal.

The earlier `0xE63Bb511028D61A9e109A5B96E344b6b47B18C33` deployment is superseded and retained only as historical evidence.

The `CommitteeGate` deployment at [`0xA558965ba50ce10E1542BaE8867f47D0B08f373a`](https://explorer-studio.genlayer.com/address/0xA558965ba50ce10E1542BaE8867f47D0B08f373a) accepted the selected member, rejected a non-member, and rejected reuse of an action ID. The contract relies on validator consensus over the public drand response; it does not verify drand threshold signatures itself.

## License

MIT
