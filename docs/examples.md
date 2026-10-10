# Business examples with recorded model output

These examples use the one-model quick start in [README.md](../README.md). In another terminal, activate the same virtual environment before calling the client. Always select `multilingual` explicitly when that is the only preloaded model.

## Support ticket routing

```bash
python example_client.py --scenario support --model multilingual
python example_client.py "The app crashes when I log in." --scenario support --model multilingual
```

The default input is `我被重复扣款了，请退款。`. The model chooses among billing, technical, and general, and separately evaluates whether a refund was requested.

An excerpt of the real response recorded on 2026-10-10:

```json
{
  "department": {
    "type": "choice",
    "choice": "billing",
    "probabilities": {"billing": 0.9982, "technical": 0.0003, "general": 0.0015},
    "confidence": 0.9869
  },
  "refund_requested": {"type": "noul", "noul": 0.9941}
}
```

This is an excerpt of `answers`, not the complete HTTP response. [Full request, response, and recording metadata](../frontend/replay/recordings/support.json).

## Agent tool selection

```bash
python example_client.py --scenario agent --model multilingual
python example_client.py "I need the installation instructions." --scenario agent --model multilingual
```

The default task reports a duplicate charge. The candidates are `search_docs`, `check_billing`, and `ask_user`. The recorded choice was `check_billing`, with candidate probability 0.8421. [Full request and response](../frontend/replay/recordings/agent.json).

The client only returns a decision. It does not call the selected tool, access billing records, or authorize a refund. Your application must implement and validate any resulting action.

## Recording provenance and interpretation

- Actual HTTP requests through the application and real Laya inference, using the multilingual checkpoint at `aa8c91ca088ec597df95a0d1c76b3063cb2ae5e8`.
- Recorded on macOS arm64, CPU, Python 3.14.6, Laya 0.3.6. The documented/CI Python version remains 3.12.
- The only redaction is the local filesystem path in `routing.repo`, replaced with `[local snapshot]/multilingual`. No API key is stored in recordings.
- These two examples are **not an accuracy evaluation**. Candidate probabilities are not task success rates; choice confidence is an entropy score. `noul` is a probability, not a boolean.
- Recorded individual timings are not a latency benchmark. The replay animation is illustrative and has its own timing.

Open [frontend/replay/index.html](../frontend/replay/index.html) locally to inspect the two recordings without installing Python or downloading a model.
