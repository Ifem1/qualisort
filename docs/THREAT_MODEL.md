# Threat model

## Malicious candidate statement

Candidate text is untrusted context and never counts as evidence by itself. The prompt explicitly forbids following instructions in candidate statements or web pages.

## Prompt injection in evidence

All evidence is quoted as data. Validators independently fetch and re-evaluate. A leader cannot make a candidate qualified merely by returning a correctly shaped object.

## Fabricated criteria masks

Masks must be within the exact criterion universe, disjoint, and total. Malformed model output fails closed to unresolved criteria.

## Unavailable evidence

If fewer than the configured minimum evidence sources are reachable, the outcome is `UNAVAILABLE`, not a guessed qualification.

Retrying an `UNAVAILABLE` candidate updates the single status record. The qualified count changes only on a transition into `QUALIFIED`, avoiding stale or duplicate eligibility counts.

## Outcome cherry-picking

`QUALIFIED` and `NOT_QUALIFIED` are terminal within a pool. Only `AMBIGUOUS` and `UNAVAILABLE` are retryable before seal.

## Owner-selected winners

The owner cannot pass a random seed. Seal commits the frozen qualified set to a future public randomness-beacon round. The committee is derived deterministically from the resulting public randomness.

## Beacon-head race

The latest beacon can advance between the leader and validator requests. The validator accepts at most a one-round difference at seal because the result is used only to choose a future round. The exact target-round randomness must later match exactly.

## Beacon trust

QualiSort does not implement threshold-signature verification for the external beacon. GenLayer consensus confirms that validators observed the same public API result. This is an explicit external trust boundary.

At seal, the leader and each validator independently fetch the current beacon head; the validator permits at most a one-round difference to handle a head advancing between requests. At draw, each independently fetches the exact committed round and must agree on that round and randomness. The direct-mode mock suite cannot establish the production consensus behavior of these external requests.

## Duplicate registration

One address can register once per pool. Candidate IDs start at one and applicant lookups are namespaced by pool.

## Selection replay

A pool can be drawn only from `SEALED`; after a draw it is terminal. Selected IDs cannot be appended twice through normal contract entry points.

## Rotation bypass

Optional `prior_selection_cap` uses the address's cumulative selection count across QualiSort pools. It is deterministic and checked at registration.
