#!/usr/bin/env python3
"""Run deterministic checks and report upstream GenVM SDK checks distinctly."""
from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENV = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
CONTRACTS = ("contracts/qualisort.py", "contracts/committee_gate.py")


def run(args: list[str]) -> tuple[int, str]:
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
    output = result.stdout.rstrip()
    if output:
        print(output, flush=True)
    print(f"exit={result.returncode}", flush=True)
    return result.returncode, output


def main() -> int:
    deterministic_failures: list[str] = []
    sdk_blocked: list[str] = []

    checks = [
        ("preflight", [sys.executable, "scripts/preflight.py"]),
        ("unit tests", [sys.executable, "-m", "pytest", "tests/unit", "-q"]),
    ]
    if shutil.which("genvm-lint"):
        checks.extend(
            (f"AST lint {contract}", ["genvm-lint", "lint", contract])
            for contract in CONTRACTS
        )
    else:
        print("BLOCKED: genvm-lint is not installed; contract lint was not run")
        sdk_blocked.append("AST lint unavailable (genvm-lint not installed)")

    try:
        import gltest  # noqa: F401
        have_gltest = True
    except Exception:
        have_gltest = False
    if have_gltest:
        checks.append(("direct tests", [sys.executable, "-m", "pytest", "tests/direct", "-q"]))
    else:
        print("BLOCKED: genlayer-test is not installed; direct tests were not run")
        deterministic_failures.append("direct tests unavailable")

    for name, args in checks:
        code, _ = run(args)
        if code:
            deterministic_failures.append(name)

    if shutil.which("genvm-lint"):
        for mode in ("validate", "schema"):
            for contract in CONTRACTS:
                args = ["genvm-lint", mode]
                if mode == "validate":
                    args.append("--json")
                args.append(contract)
                code, output = run(args)
                label = f"{mode} {contract}"
                if code == 0:
                    print(f"PASS: GenVM SDK {label}", flush=True)
                elif code == 3 or "Failed to load SDK" in output or '"code":"E101"' in output:
                    print(
                        f"BLOCKED: GenVM SDK {label} (upstream SDK artifact unavailable; exit {code})",
                        flush=True,
                    )
                    sdk_blocked.append(f"{label}: {output}")
                else:
                    print(f"FAIL: GenVM SDK {label} (exit {code})", flush=True)
                    deterministic_failures.append(label)

    print("\nQUALITY GATE SUMMARY", flush=True)
    print("Deterministic checks: " + ("FAIL" if deterministic_failures else "PASS"), flush=True)
    for failure in deterministic_failures:
        print(f"  FAIL: {failure}", flush=True)
    if sdk_blocked:
        print("GenVM SDK checks: BLOCKED", flush=True)
        for blocked in sdk_blocked:
            print(f"  BLOCKED: {blocked}", flush=True)
    elif shutil.which("genvm-lint"):
        print("GenVM SDK validation/schema: PASS", flush=True)

    if deterministic_failures:
        return 1
    if sdk_blocked:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
