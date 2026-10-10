import importlib.util
from pathlib import Path

import pytest


def load_client():
    spec = importlib.util.spec_from_file_location("example_client", Path(__file__).parents[1] / "example_client.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "build_payload"), "Missing reusable business scenarios"
    return module


@pytest.mark.parametrize("scenario,question,labels", [
    ("support", "department", {"billing", "technical", "general"}),
    ("agent", "next_action", {"search_docs", "check_billing", "ask_user"}),
])
def test_business_scenarios_use_the_selected_model(scenario, question, labels):
    module = load_client()
    payload = module.build_payload("Please refund the duplicate charge.", scenario, "multilingual")
    assert payload["model"] == "multilingual"
    assert "Please refund" in str(payload["state"])
    assert payload["questions"][question]["type"] == "choice"
    assert set(payload["questions"][question]["criteria"]) == labels


def test_original_refund_example_is_preserved():
    module = load_client()
    payload = module.build_payload("refund please", "refund", None)
    assert "model" not in payload
    assert payload["questions"]["refund_requested"]["type"] == "noul"
    assert payload["questions"]["urgency"]["type"] == "score"
