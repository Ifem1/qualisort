# v0.2.18
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


@gl.contract_interface
class IQualiSort:
    class View:
        def is_selected(self, pool_id: u256, applicant: Address) -> bool: ...

    class Write:
        pass


class ActionAccepted(gl.Event):
    def __init__(self, action_id: str, member: Address, /, **blob): ...


class CommitteeGate(gl.Contract):
    """Tiny consumer proving that a QualiSort committee can gate another IC."""

    qualisort: Address
    pool_id: u256
    used_actions: TreeMap[str, bool]

    def __init__(self, qualisort: Address, pool_id: u256):
        self.qualisort = qualisort
        self.pool_id = pool_id

    @gl.public.view
    def is_authorized(self, member: Address) -> bool:
        contract = IQualiSort(self.qualisort)
        return bool(contract.view().is_selected(self.pool_id, member))

    @gl.public.write
    def perform(self, action_id: str) -> None:
        value = " ".join(str(action_id).split())[:128]
        if value == "":
            raise gl.vm.UserError("EXPECTED: action_id required")
        if self.used_actions.get(value):
            raise gl.vm.UserError("EXPECTED: action already used")
        contract = IQualiSort(self.qualisort)
        if not contract.view().is_selected(self.pool_id, gl.message.sender_address):
            raise gl.vm.UserError("EXPECTED: sender is not selected committee member")
        self.used_actions[value] = True
        ActionAccepted(value, gl.message.sender_address).emit()
