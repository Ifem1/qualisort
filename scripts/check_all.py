#!/usr/bin/env python3
from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENV = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
CONTRACTS = ("contracts/qualisort.py", "contracts/committee_gate.py")


def call(args: list[str]) -> int:
    print("+", " ".join(args), flush=True)
    result = subprocess.run(args, cwd=ROOT, check=False, env=ENV)
    return result.returncode


def captured(args: list[str]) -> int:
    print("+", " ".join(args), flush=True)
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        env=ENV,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.stdout:
        print(result.stdout.rstrip(), flush=True)
    print(f"exit={result.returncode}", flush=True)
    return result.returncode


def main() -> int:
    if call([sys.executable, "scripts/preflight.py"]):
        return 1
    if call([sys.executable, "-m", "pytest", "tests/unit", "-q"]):
        return 1

    if shutil.which("genvm-lint"):
        for contract in CONTRACTS:
            if call(["genvm-lint", "lint", contract]):
                return 1

        for mode in ("validate", "schema"):
            for contract in CONTRACTS:
                args = ["genvm-lint", mode]
                if mode == "validate":
                    args.append("--json")
                args.append(contract)
                code = captured(args)
                if code in (1, 2):
                    return 1
                if code not in (0, 3):
                    print(f"ERROR: unexpected genvm-lint {mode} exit code {code}")
                    return 1
                if code == 3:
                    print(
                        f"BLOCKED: genvm-lint {mode} could not obtain the required upstream SDK artifact",
                        flush=True,
                    )
    else:
        print("SKIP: genvm-lint not installed")

    try:
        import gltest  # noqa: F401
        have_gltest = True
    except Exception:
        have_gltest = False

    if have_gltest:
        if call([sys.executable, "-m", "pytest", "tests/direct", "-q"]):
            return 1
    else:
        print("SKIP: genlayer-test not installed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
