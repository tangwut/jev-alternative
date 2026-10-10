"""Call the resident model service without printing the API key."""
import argparse
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv


DEFAULT_TEXT = {
    "refund": "我被重复扣款了，请帮我退款。",
    "support": "我被重复扣款了，请退款。",
    "agent": "A customer reports a duplicate charge. Choose which tool to use next.",
}


def build_payload(text, scenario="refund", model=None):
    payload = {
        "state": {"message": text},
        "questions": {
            "refund_requested": {"type": "noul", "instructions": "Does the customer request a refund?"},
            "urgency": {"type": "score", "instructions": "How urgent is the request?",
                        "criteria": ["no time pressure", "needs attention soon", "critical deadline"]},
        },
    }
    if scenario == "support":
        payload["questions"] = {
            "department": {"type": "choice", "instructions": "Which department should handle this request?",
                           "criteria": {"billing": "payments, duplicate charges and refunds",
                                        "technical": "software bugs and outages", "general": "other inquiries"}},
            "refund_requested": {"type": "noul", "instructions": "Does the customer request a refund?"},
        }
    elif scenario == "agent":
        payload["questions"] = {
            "next_action": {"type": "choice", "instructions": "Choose the next tool for handling the task.",
                            "criteria": {"search_docs": "look up product documentation",
                                         "check_billing": "inspect payment records and duplicate charges",
                                         "ask_user": "request missing details from the user"}},
        }
    elif scenario != "refund":
        raise ValueError("Unknown scenario")
    if model:
        payload["model"] = model
    return payload


def main():
    load_dotenv(Path(__file__).resolve().with_name(".env"))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", nargs="?")
    parser.add_argument("--scenario", choices=tuple(DEFAULT_TEXT), default="refund")
    parser.add_argument("--url", default="http://127.0.0.1:8000")
    parser.add_argument("--model", choices=["english", "multilingual", "typed-decisions"])
    args = parser.parse_args()
    key = os.environ.get("LAYA_API_KEY", "").strip()
    if not key:
        parser.exit(1, "Set LAYA_API_KEY in .env or run python scripts/setup_local.py first.\n")
    payload = build_payload(args.text or DEFAULT_TEXT[args.scenario], args.scenario, args.model)
    request = Request(args.url.rstrip("/") + "/api/v1/systemone",
                      data=json.dumps(payload).encode(),
                      headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
    try:
        with urlopen(request, timeout=120) as response:
            print(json.dumps(json.load(response), ensure_ascii=False, indent=2))
    except HTTPError as error:
        parser.exit(1, f"API returned HTTP {error.code}; check the key, selected model and server logs.\n")
    except (URLError, TimeoutError):
        parser.exit(1, "Cannot reach the API; start python main.py and wait for /health to report ready.\n")


if __name__ == "__main__":
    main()
