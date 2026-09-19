"""Direct-mode checks for CommitteeGate invariants that do not require cross-contract dispatch."""

CONTRACT = "contracts/committee_gate.py"


def test_empty_action_id_fails_before_cross_contract_call(
    direct_vm, direct_deploy, direct_alice
):
    gate = direct_deploy(CONTRACT, direct_alice, 2)
    with direct_vm.expect_revert("action_id required"):
        gate.perform("   ")
