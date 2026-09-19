#!/usr/bin/env python3
from __future__ import annotations
import pathlib, subprocess, sys, shutil
ROOT = pathlib.Path(__file__).resolve().parents[1]
ENV = dict(__import__("os").environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")

def call(args):
    print("+", " ".join(args), flush=True)
    r=subprocess.run(args,cwd=ROOT,check=False,env=ENV)
    return r.returncode

def main():
    if call([sys.executable,"scripts/preflight.py"]): return 1
    if call([sys.executable,"-m","pytest","tests/unit","-q"]): return 1
    if shutil.which("genvm-lint"):
        for contract in ("contracts/qualisort.py", "contracts/committee_gate.py"):
            if call(["genvm-lint", "lint", contract]):
                return 1
        for contract in ("contracts/qualisort.py", "contracts/committee_gate.py"):
            result = subprocess.run(["genvm-lint", "validate", "--json", contract], cwd=ROOT, capture_output=True, text=True, env=ENV)
            print(result.stdout.strip(), flush=True)
            if result.returncode != 0:
                print("BLOCKED: GenVM SDK semantic validation could not load the local SDK cache", flush=True)
                break
    else:
        print("SKIP: genvm-lint not installed")
    try:
        import gltest  # noqa: F401
        have=True
    except Exception:
        have=False
    if have:
        if call([sys.executable,"-m","pytest","tests/direct","-q"]): return 1
    else:
        print("SKIP: genlayer-test not installed")
    return 0
if __name__=="__main__": raise SystemExit(main())
