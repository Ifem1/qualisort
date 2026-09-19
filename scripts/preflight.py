#!/usr/bin/env python3
from __future__ import annotations
import ast
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "qualisort.py"
STABLE_RPC = "https://studio.genlayer.com/api"
STABLE_CHAIN = "61999"


def main() -> int:
    failures: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".py", ".md", ".yaml", ".yml", ".json", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if path != Path(__file__) and "61997" in text:
            failures.append(f"wrong chain ID in {path.relative_to(ROOT)}")
    text = CONTRACT.read_text(encoding="utf-8")
    try:
        ast.parse(text)
    except SyntaxError as exc:
        failures.append(f"contract syntax error: {exc}")
    for required in (
        "run_nondet_unsafe",
        "qualification_status",
        "DRAND_LATEST_URL",
        "selection_seed",
        "is_selected",
    ):
        if required not in text:
            failures.append(f"missing contract invariant marker: {required}")
    repo_text = "\n".join(
        p.read_text(encoding="utf-8", errors="ignore")
        for p in ROOT.rglob("*")
        if p.is_file() and p.suffix.lower() in {".py", ".md", ".yaml", ".yml", ".json", ".txt"}
    )
    if STABLE_RPC not in repo_text or STABLE_CHAIN not in repo_text:
        failures.append("Studionet RPC/chain declaration missing")
    if failures:
        print("PREFLIGHT FAILED")
        for item in failures:
            print("-", item)
        return 1
    print("PREFLIGHT OK")
    print(f"network: {STABLE_CHAIN} {STABLE_RPC}")
    print("contract: contracts/qualisort.py")
    print("frontend: none")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
