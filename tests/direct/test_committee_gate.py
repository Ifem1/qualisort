"""Direct-mode checks for CommitteeGate invariants that do not require cross-contract dispatch."""

CONTRACT = "contracts/committee_gate.py"


def test_empty_action_id_fails_before_cross_contract_call(
    direct_vm, direct_deploy, direct_alice
):
    # Load the matching SDK without registering another contract class. Use
    # its Address wrapper because the constructor requires a typed IC address.
    from pathlib import Path

    from gltest.direct.sdk_loader import setup_sdk_paths

    setup_sdk_paths(Path(CONTRACT))
    from genlayer import Address

    gate = direct_deploy(CONTRACT, Address(direct_alice), 2)
    with direct_vm.expect_revert("action_id required"):
        gate.perform("   ")
