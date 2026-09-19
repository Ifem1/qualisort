# Architecture

QualiSort deliberately separates **eligibility** from **selection**.

## 1. Immutable pool policy

`create_pool` canonicalises a bounded JSON rubric. Up to six criteria are stored in deterministic order. Required criteria and the minimum pass count become immutable pool state.

## 2. Candidate registration

Each address may register once per pool with a bounded statement and 1–3 HTTPS evidence URLs. Private/local/ambiguous host shapes are rejected before any nondeterministic call.

## 3. Consensus qualification

`assess_candidate` runs a custom leader/validator equivalence path. Both sides independently:

1. fetch the frozen evidence URLs;
2. treat page content as hostile data;
3. map every rubric criterion to PASS / FAIL / UNRESOLVED;
4. return total disjoint bitmasks.

Validators compare qualification-affecting fields, not prose.

## 4. Deterministic eligibility state

Contract code derives the final candidate status from masks, required criteria, minimum pass count, and minimum reachable evidence sources.

## 5. Pool seal

Only a pool owner can seal, and only when there are enough qualified candidates. Sealing observes the public randomness-beacon head under consensus and commits to a future target round. The pool digest binds the full policy and qualified candidate set.

## 6. Committee draw

Anyone can trigger the draw once the target round is published. Validators independently fetch the exact target beacon output. The contract derives a seed and deterministic per-candidate hash scores, sorts only the qualified set, and stores the first N members.

## 7. Consumer surface

Other ICs can synchronously call `is_selected`, `is_qualified`, or `get_committee`. The companion `CommitteeGate` demonstrates this boundary without introducing a frontend or application flow.

## Assessment retry accounting

Only `REGISTERED`, `AMBIGUOUS`, and `UNAVAILABLE` candidates can be assessed. A candidate increments `qualified_count` only when its status transitions into `QUALIFIED`; terminal outcomes cannot be retried. This prevents an unavailable-to-qualified retry from being counted more than once.
