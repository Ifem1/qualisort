# Studionet deployment

Target only:

- chain ID: **61999**
- RPC: `https://studio.genlayer.com/api`
- explorer: `https://explorer-studio.genlayer.com/`

## Before deployment

```bash
python scripts/preflight.py
pytest tests/unit -q
python -m pip install -r requirements-test.txt
pytest tests/direct -q
```

Linter AST pass:

```bash
genvm-lint check contracts/qualisort.py
genvm-lint check contracts/committee_gate.py
```

## Deploy the primitive

```bash
python scripts/deploy_studionet.py
```

or:

```bash
genlayer deploy --contract contracts/qualisort.py --rpc https://studio.genlayer.com/api
```

The command requires the configured CLI account to be unlocked and reachable Studionet RPC. The deployed address is [`0xE63Bb511028D61A9e109A5B96E344b6b47B18C33`](https://explorer-studio.genlayer.com/address/0xE63Bb511028D61A9e109A5B96E344b6b47B18C33), and the deployment transaction finalized successfully. See [`LIVE_EVIDENCE.md`](LIVE_EVIDENCE.md) for the transaction and lifecycle receipts.

## Optional consumer proof

Deploy `CommitteeGate` after a QualiSort pool is drawn. Constructor arguments are the finalized QualiSort address and the pool ID.

The consumer is not a frontend and is not the primary submission. It exists to prove that selected committee membership is directly reusable by another Intelligent Contract.

## Post-deployment evidence

The recorded deployment and consumer proof are in [`LIVE_EVIDENCE.md`](LIVE_EVIDENCE.md). Add evidence there only after observing finalized receipts and verifying explorer links. Never invent addresses, hashes, or explorer links.
