# Finalized Studionet evidence

Observed on 2026-09-19 against GenLayer Studionet, chain ID **61999**.

## Corrected deployment superseding the prior address

The earlier deployment below is superseded because it contained the adjacent-head consensus flaw: seal validation tolerated a one-round difference in the independently observed latest drand head. The corrected source requires exact head-round equality before committing the future target.

- Corrected address: [`0xc6e4D96274137f4b0C432e9b42E0a1D80C20D872`](https://explorer-studio.genlayer.com/address/0xc6e4D96274137f4b0C432e9b42E0a1D80C20D872)
- Deployment transaction: [`0xfc05b5353d2a10ed229183ca7ea0161df2610d22dd894b49c25d927194a0f48c`](https://explorer-studio.genlayer.com/tx/0xfc05b5353d2a10ed229183ca7ea0161df2610d22dd894b49c25d927194a0f48c)
- Network: Studionet chain 61999; receipt status: **FINALIZED**; consensus result: `MAJORITY_AGREE`; deployment execution: `SUCCESS`.
- The CLI source retrieval for the corrected address matches `contracts/qualisort.py` byte-for-byte after removing the CLI's `Result:` wrapper and normalizing line endings.
- A new post-fix lifecycle was not fabricated in this run; the corrected deployment was finalized and source-matched, but pool/seal/draw transactions remain to be exercised against this new address.

## Network and explorer

- RPC: `https://studio.genlayer.com/api`
- Explorer: [GenLayer Studio Explorer](https://explorer-studio.genlayer.com/)
- Transaction links below use the explorer's verified `/tx/<hash>` route.

## QualiSort deployment

- Address: [`0xE63Bb511028D61A9e109A5B96E344b6b47B18C33`](https://explorer-studio.genlayer.com/address/0xE63Bb511028D61A9e109A5B96E344b6b47B18C33)
- Deployment transaction: [`0xf2521360b5277fd6ef4b2cfb4a7a7d0b546934b75465e902dab2970df083fa1f`](https://explorer-studio.genlayer.com/tx/0xf2521360b5277fd6ef4b2cfb4a7a7d0b546934b75465e902dab2970df083fa1f) — **FINALIZED**, deployment execution succeeded.
- Deployer: `0x7876E9F76F32925c212528D57BC9DfE5E34bCC07`.
- The deployed ABI was retrieved from Studionet and includes the documented pool, assessment, sealing, draw, and membership methods.

## Live lifecycle: pool 2

Pool 2 was used for the recorded lifecycle. It has one required criterion (`PUBLIC_REPO`): the evidence URL must resolve to a public software repository page with a project description and publicly listed source files. The pool has committee size 1, minimum pass 1, and one required evidence source.

| Step | Transaction | Finalized result |
|---|---|---|
| Create pool 2 | [`0x802807a5277d0d04c7d2eb1434c8d7936e3c0fb44104ddf265ef1e31ff8ff758`](https://explorer-studio.genlayer.com/tx/0x802807a5277d0d04c7d2eb1434c8d7936e3c0fb44104ddf265ef1e31ff8ff758) | `OPEN`, pool ID 2 |
| Register candidate 1 | [`0x4294b2d20d0746983d933206e70ac1c1866280906db5cce9dfb54d39d024ad93`](https://explorer-studio.genlayer.com/tx/0x4294b2d20d0746983d933206e70ac1c1866280906db5cce9dfb54d39d024ad93) | Applicant `0x7876E9F76F32925c212528D57BC9DfE5E34bCC07`; evidence [`https://github.com/torvalds/linux`](https://github.com/torvalds/linux) |
| Assess candidate 1 | [`0x5e79f99b8f59057833caadafb7565ca3edcd27ec228907d0bcc080d7990553d7`](https://explorer-studio.genlayer.com/tx/0x5e79f99b8f59057833caadafb7565ca3edcd27ec228907d0bcc080d7990553d7) | `QUALIFIED`; pass mask 1, fail mask 0, unresolved mask 0 |
| Register candidate 2 | [`0x05209fe274d3dd413c62fd9376fa5fefe595eb10ac739399748d30058d438d5b`](https://explorer-studio.genlayer.com/tx/0x05209fe274d3dd413c62fd9376fa5fefe595eb10ac739399748d30058d438d5b) | Applicant `0xA49c51d759790116D451f256654dD9F0549D341F`; evidence [`https://example.com`](https://example.com) |
| Assess candidate 2 | [`0xca0c30c31893511b2272fe2ec93969b2aca4214aa958d29f0ebe8ed809d49353`](https://explorer-studio.genlayer.com/tx/0xca0c30c31893511b2272fe2ec93969b2aca4214aa958d29f0ebe8ed809d49353) | `AMBIGUOUS`; pass mask 0, fail mask 0, unresolved mask 1. Validator rationale says the unrelated page does not directly show a repository; the candidate statement is not proof. |
| Seal pool 2 | [`0x5b81a7b5025f0f8f7a8646a617805763bd1e0aea6957c069e7403e3d6704a6e9`](https://explorer-studio.genlayer.com/tx/0x5b81a7b5025f0f8f7a8646a617805763bd1e0aea6957c069e7403e3d6704a6e9) | `SEALED`; qualified count 1; target drand round 6,480,746; pool digest `891b138f5b76772b838b50c4d1254363806d892b7c25ac0db60cf16f3b69ebab` |
| Draw committee | [`0xeec47a367cf4674db926fbe636390580f1ae7200319d27cc6b65a5fe567f1ac6`](https://explorer-studio.genlayer.com/tx/0xeec47a367cf4674db926fbe636390580f1ae7200319d27cc6b65a5fe567f1ac6) | `DRAWN`; selected candidate ID 1 |

After sealing, the exact public drand endpoint returned round `6480746` with randomness `a38b0e1dcb674ce1ddc3dded1b97049da1b67938ce177294ca4f7145bef9c1f4`. The finalized pool view stores that same randomness and target round. It stores selection seed `2138401b3eb5b487f7f178975297a7fd0e4eebc29f04a57cb690472d0c29d9f9`.

The finalized `get_committee(2)` view returned candidate 1 and applicant `0x7876E9F76F32925c212528D57BC9DfE5E34bCC07`. `is_selected(2, applicant)` returned `true` for that account and `false` for candidate 2.

## CommitteeGate consumer proof

- Corrected deployment address: [`0xA558965ba50ce10E1542BaE8867f47D0B08f373a`](https://explorer-studio.genlayer.com/address/0xA558965ba50ce10E1542BaE8867f47D0B08f373a).
- Deployment transaction: [`0x0cf91d952f2eed2b1802348857901aeb2ddfc25ae5d894ac19eeffe3d953e67d`](https://explorer-studio.genlayer.com/tx/0x0cf91d952f2eed2b1802348857901aeb2ddfc25ae5d894ac19eeffe3d953e67d) — **FINALIZED**, constructor succeeded.
- `is_authorized` returned `true` for candidate 1 and `false` for candidate 2.
- Selected member action `qualisort-live-action-2`: [`0xf0bd4b1c69d399ffa3fc5ee62b0459ad32cd583478c50d85cb7fb96df8a9d4b6`](https://explorer-studio.genlayer.com/tx/0xf0bd4b1c69d399ffa3fc5ee62b0459ad32cd583478c50d85cb7fb96df8a9d4b6) — **FINALIZED**, leader execution `SUCCESS`.
- Replaying the same action: [`0xab2225ab70b03f0da909306223c8ed07dc287a42369d009a02c19d7c347f7d37`](https://explorer-studio.genlayer.com/tx/0xab2225ab70b03f0da909306223c8ed07dc287a42369d009a02c19d7c347f7d37) — **FINALIZED**, execution rolled back with `EXPECTED: action already used`.
- Candidate 2 non-member action: [`0xc4a57ffe439b223e803352ef5da92bb91f77080079f131f42dc2bcd5faadc3fc`](https://explorer-studio.genlayer.com/tx/0xc4a57ffe439b223e803352ef5da92bb91f77080079f131f42dc2bcd5faadc3fc) — **FINALIZED**, execution rolled back with `EXPECTED: sender is not selected committee member`.

## Trust boundary and scope

The contract’s drand values above were observed from the public API independently under GenLayer consensus. QualiSort does not verify the beacon’s threshold signature on-chain. The account’s evidence qualifies the submitted address for this one pool; it does not prove the real-world identity of the account owner.

Pool 1 is an unused open pool created while resolving CLI argument encoding. The recorded lifecycle and all transaction evidence above refer to pool 2. An initial CommitteeGate deployment transaction also finalized at the consensus layer but its constructor execution failed due to an address type mismatch; it did not create the corrected consumer deployment listed above.
