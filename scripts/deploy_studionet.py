#!/usr/bin/env python3
"""Deploy QualiSort to GenLayer Studionet using the active CLI account."""
from __future__ import annotations
import pathlib, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "qualisort.py"
PREFLIGHT = ROOT / "scripts" / "preflight.py"
STUDIONET_RPC = "https://studio.genlayer.com/api"
EXPECTED_CHAIN_ID = "61999"


def run(command: list[str]) -> None:
    print("+", " ".join(command), flush=True)
    done = subprocess.run(command, cwd=ROOT, check=False)
    if done.returncode != 0:
        raise SystemExit(done.returncode)


def main() -> int:
    cli = shutil.which("genlayer")
    if cli is None:
        print("ERROR: genlayer CLI is not installed or not on PATH", file=sys.stderr)
        return 2
    run([sys.executable, str(PREFLIGHT)])
    print(f"Target: Studionet chain {EXPECTED_CHAIN_ID} at {STUDIONET_RPC}")
    run([cli, "account", "show"])
    run([cli, "deploy", "--contract", str(CONTRACT), "--rpc", STUDIONET_RPC])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
