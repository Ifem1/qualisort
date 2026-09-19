"""Shared direct-mode configuration for QualiSort."""
import os
import pytest


if os.name == "nt":
    # genlayer-test 0.29.2 unlinks an fd-0 tempfile while Windows still has it
    # open. Keep the same implementation but omit that POSIX-only cleanup.
    from gltest.direct import loader, pytest_plugin

    _original = loader._inject_message_to_fd0
    _source = __import__("inspect").getsource(_original)
    _source = _source.replace("os.unlink(path)", "pass  # Windows holds stdin open")
    _scope = {"__name__": loader.__name__, "os": os, "tempfile": __import__("tempfile")}
    exec(compile(_source, __import__("inspect").getsourcefile(_original), "exec"), _scope)
    loader._inject_message_to_fd0 = _scope["_inject_message_to_fd0"]
    pytest_plugin.deploy_contract.__globals__["_inject_message_to_fd0"] = loader._inject_message_to_fd0


@pytest.fixture(autouse=True)
def _reset_contract_registry():
    yield
    try:
        import genlayer.gl.genvm_contracts as contracts
    except ImportError:
        return
    contracts.__known_contract__ = None
