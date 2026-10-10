(function () {
const recordings = {
  "metadata": {
    "recorded_on": "2026-10-10",
    "model_revision": "aa8c91ca088ec597df95a0d1c76b3063cb2ae5e8",
    "device": "cpu",
    "platform": "Darwin arm64",
    "python": "3.14.6",
    "laya": "0.3.6",
    "startup_seconds": 37.23,
    "notice": "Recorded HTTP responses from real local inference. Replay does not run a model. Individual timings are not a benchmark.",
    "redactions": [
      "routing.repo: local filesystem path replaced with [local snapshot]/multilingual"
    ]
  },
  "records": [
    {
      "id": "support",
      "request": {
        "state": {
          "message": "我被重复扣款了，请退款。"
        },
        "questions": {
          "department": {
            "type": "choice",
            "instructions": "Which department should handle this request?",
            "criteria": {
              "billing": "payments, duplicate charges and refunds",
              "technical": "software bugs and outages",
              "general": "other inquiries"
            }
          },
          "refund_requested": {
            "type": "noul",
            "instructions": "Does the customer request a refund?"
          }
        },
        "model": "multilingual"
      },
      "response": {
        "model": "laya-rl-agent",
        "answers": {
          "department": {
            "type": "choice",
            "choice": "billing",
            "probabilities": {
              "billing": 0.9982,
              "technical": 0.0003,
              "general": 0.0015
            },
            "confidence": 0.9869,
            "action": {
              "act_probability": 1.0
            }
          },
          "refund_requested": {
            "type": "noul",
            "noul": 0.9941,
            "confidence": 0.9941,
            "action": {
              "act_probability": 1.0
            }
          }
        },
        "usage": {
          "input_tokens": 98,
          "output_tokens": 0
        },
        "routing": {
          "model": "multilingual",
          "repo": "[local snapshot]/multilingual",
          "reason": "explicit model='multilingual'",
          "detection": null,
          "workflow": null
        }
      },
      "elapsed_ms": 62.68
    },
    {
      "id": "agent",
      "request": {
        "state": {
          "message": "A customer reports a duplicate charge. Choose which tool to use next."
        },
        "questions": {
          "next_action": {
            "type": "choice",
            "instructions": "Choose the next tool for handling the task.",
            "criteria": {
              "search_docs": "look up product documentation",
              "check_billing": "inspect payment records and duplicate charges",
              "ask_user": "request missing details from the user"
            }
          }
        },
        "model": "multilingual"
      },
      "response": {
        "model": "laya-rl-agent",
        "answers": {
          "next_action": {
            "type": "choice",
            "choice": "check_billing",
            "probabilities": {
              "search_docs": 0.0546,
              "check_billing": 0.8421,
              "ask_user": 0.1033
            },
            "confidence": 0.5104,
            "action": {
              "act_probability": 1.0
            }
          }
        },
        "usage": {
          "input_tokens": 66,
          "output_tokens": 0
        },
        "routing": {
          "model": "multilingual",
          "repo": "[local snapshot]/multilingual",
          "reason": "explicit model='multilingual'",
          "detection": null,
          "workflow": null
        }
      },
      "elapsed_ms": 43.25
    }
  ]
};
if (typeof module !== "undefined" && module.exports) module.exports = recordings;
if (typeof window !== "undefined") window.LayaRecordings = recordings;
})();
