"""Structural security checks for selection and CommitteeGate boundaries."""
from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[2]
QUALISORT = ROOT / "contracts" / "qualisort.py"
GATE = ROOT / "contracts" / "committee_gate.py"


def _class_function_source(path: Path, class_name: str, function_name: str) -> str:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    klass = next(
        node for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == class_name
    )
    fn = next(
        node for node in klass.body
        if isinstance(node, ast.FunctionDef) and node.name == function_name
    )
    return ast.get_source_segment(source, fn) or ""


def test_pool_digest_binds_all_selection_relevant_frozen_state():
    body = _class_function_source(QUALISORT, "QualiSort", "_pool_digest")
    for marker in (
        "pool_id",
        "pool.owner",
        "pool.name",
        "pool.domain",
        "pool.criteria_json",
        "pool.required_mask",
        "pool.min_pass",
        "pool.min_evidence_sources",
        "pool.committee_size",
        "pool.prior_selection_cap",
        "target_round",
        "candidate.status",
        "candidate.applicant",
        "candidate.pass_mask",
    ):
        assert marker in body
    assert "CANDIDATE_QUALIFIED" in body


def test_draw_has_no_caller_seed_or_model_ordering_path():
    source = QUALISORT.read_text(encoding="utf-8")
    tree = ast.parse(source)
    klass = next(
        node for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "QualiSort"
    )
    fn = next(
        node for node in klass.body
        if isinstance(node, ast.FunctionDef) and node.name == "draw_committee"
    )
    assert [arg.arg for arg in fn.args.args] == ["self", "pool_id"]
    body = ast.get_source_segment(source, fn) or ""
    assert "CANDIDATE_QUALIFIED" in body
    assert "ranked.sort()" in body
    assert "exec_prompt" not in body
    assert "_beacon_randomness(target_round)" in body
    assert "selection_seed(str(pool.pool_digest), target_round, randomness)" in body


def test_committee_gate_is_a_fixed_typed_consumer_and_marks_replay_after_auth():
    source = GATE.read_text(encoding="utf-8")
    tree = ast.parse(source)
    klass = next(
        node for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "CommitteeGate"
    )
    init = next(
        node for node in klass.body
        if isinstance(node, ast.FunctionDef) and node.name == "__init__"
    )
    perform = next(
        node for node in klass.body
        if isinstance(node, ast.FunctionDef) and node.name == "perform"
    )
    init_body = ast.get_source_segment(source, init) or ""
    perform_body = ast.get_source_segment(source, perform) or ""

    assert "self.qualisort = qualisort" in init_body
    assert "self.pool_id = pool_id" in init_body
    assert "contract = IQualiSort(self.qualisort)" in perform_body
    assert "contract.view().is_selected(self.pool_id, gl.message.sender_address)" in perform_body
    assert perform_body.index("sender is not selected committee member") < perform_body.index(
        "self.used_actions[value] = True"
    )

    protected_assignments = []
    for node in ast.walk(klass):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if (
                isinstance(target, ast.Attribute)
                and isinstance(target.value, ast.Name)
                and target.value.id == "self"
                and target.attr in {"qualisort", "pool_id"}
            ):
                protected_assignments.append(node)
    init_nodes = set(ast.walk(init))
    assert protected_assignments
    assert all(node in init_nodes for node in protected_assignments)


def test_no_forbidden_network_alias_is_stored_in_repository_text():
    stable_chain = "61999"
    forbidden = (
        str(int(stable_chain) - 2),
        "studio" + " dev",
        "studio" + "-dev",
        "studio" + " next",
        "studio" + "-next",
        "brad" + "bury",
    )
    text_files = {".py", ".md", ".yaml", ".yml", ".json", ".txt"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in text_files:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for token in forbidden:
            assert token.lower() not in text, f"forbidden network token in {path.relative_to(ROOT)}"
