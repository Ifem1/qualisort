#!/usr/bin/env python3
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = (
    ROOT / "contracts" / "qualisort.py",
    ROOT / "contracts" / "committee_gate.py",
)
STABLE_RPC = "https://studio.genlayer.com/api"
STABLE_CHAIN = "61999"
TEXT_SUFFIXES = {".py", ".md", ".yaml", ".yml", ".json", ".txt"}


def _forbidden_network_tokens() -> tuple[str, ...]:
    return (
        str(int(STABLE_CHAIN) - 2),
        "studio" + " dev",
        "studio" + "-dev",
        "studio" + " next",
        "studio" + "-next",
        "brad" + "bury",
    )


def main() -> int:
    failures: list[str] = []
    texts: list[tuple[Path, str]] = []

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        texts.append((path, content))
        lowered = content.lower()
        for token in _forbidden_network_tokens():
            if token.lower() in lowered:
                failures.append(
                    f"forbidden network reference {token!r} in {path.relative_to(ROOT)}"
                )

    for contract in CONTRACTS:
        try:
            ast.parse(contract.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            failures.append(f"{contract.relative_to(ROOT)} syntax error: {exc}")

    primary = CONTRACTS[0].read_text(encoding="utf-8")
    for required in (
        "run_nondet_unsafe",
        "qualification_status",
        "DRAND_LATEST_URL",
        "selection_seed",
        "is_selected",
    ):
        if required not in primary:
            failures.append(f"missing contract invariant marker: {required}")

    repo_text = "\n".join(content for _, content in texts)
    if STABLE_RPC not in repo_text or STABLE_CHAIN not in repo_text:
        failures.append("Studionet RPC/chain declaration missing")

    config = (ROOT / "gltest.config.yaml").read_text(encoding="utf-8")
    if "default: studionet" not in config or STABLE_RPC not in config:
        failures.append("gltest.config.yaml is not pinned to Studionet")
    if config.count("studionet:") != 1:
        failures.append("gltest.config.yaml must define exactly one Studionet network")

    for name in ("frontend", "web", "app", "public"):
        if (ROOT / name).exists():
            failures.append(f"frontend/web-app scaffolding present: {name}/")

    if failures:
        print("PREFLIGHT FAILED")
        for item in failures:
            print("-", item)
        return 1

    print("PREFLIGHT OK")
    print(f"network: {STABLE_CHAIN} {STABLE_RPC}")
    print("contracts: contracts/qualisort.py, contracts/committee_gate.py")
    print("frontend: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
