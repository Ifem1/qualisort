"""Cheap repository-level checks that run without GenLayer dependencies."""
from pathlib import Path
import ast
import json

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "contracts" / "qualisort.py"


def test_contract_parses_as_python():
    ast.parse(CONTRACT.read_text(encoding="utf-8"))


def test_network_is_studionet_only():
    import yaml
    config = yaml.safe_load((ROOT / "gltest.config.yaml").read_text(encoding="utf-8"))
    assert config["networks"]["default"] == "studionet"
    assert set(config["networks"]) == {"default", "studionet"}
    assert config["networks"]["studionet"]["url"] == "https://studio.genlayer.com/api"
    all_text = "\n".join(
        p.read_text(encoding="utf-8", errors="ignore")
        for p in ROOT.rglob("*")
        if p.is_file() and p.suffix in {".py", ".md", ".yaml", ".yml", ".json", ".txt"}
    )
    assert "61999" in all_text
    assert "https://studio.genlayer.com/api" in all_text


def test_no_frontend_tree():
    banned = {"frontend", "web", "app", "src/components", "public"}
    paths = {str(p.relative_to(ROOT)).lower() for p in ROOT.rglob("*") if p.is_dir()}
    assert not any(item in paths for item in banned)


def test_contract_has_custom_validator_and_future_beacon():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "run_nondet_unsafe" in text
    assert "BEACON_DELAY_ROUNDS" in text
    assert "DRAND_LATEST_URL" in text
    assert "qualification_status" in text
    assert "selection_seed" in text


def test_example_config_is_valid():
    data = json.loads((ROOT / "examples" / "criteria.json").read_text())
    assert 1 <= len(data) <= 6
    assert all("id" in x and "description" in x and "required" in x for x in data)
