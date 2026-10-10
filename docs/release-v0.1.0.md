# v0.1.0 — Local decisions, easier first use

Release notes prepared for review. Publish only after the onboarding change is integrated and CI is green on the release commit.

## What is included

- Authenticated, resident Laya HTTP API for choice, score, and proposition questions.
- English README and Chinese documentation, with separate quick-start and operations guidance.
- Single-model setup: pinned Hugging Face download, SHA-256 verification, private generated key, and preservation of existing configuration.
- Support-ticket routing and Agent tool-selection client scenarios.
- Offline replay of two real local model responses, with recording metadata and disclosed path redaction.
- A short Tetris preview under 0.5 MB, alongside the original recordings and live Tetris/Snake demos.
- Interactive Swagger documentation for the inference endpoint.
- Contribution roadmap and issue/PR templates.

## Getting started

Use the one-model multilingual quick start in README.md. It needs Python 3.12, network access for the first dependency/model download, disk space, and RAM. For live games, prepare the English model instead.

## Validation scope

The automated checks exercise HTTP authentication, request validation, startup/shutdown, concurrency, local configuration preparation, client payloads, game logic, and offline replay. Real multilingual inference was exercised on macOS arm64 CPU with Python 3.14.6. This is not a Windows/Linux/GPU runtime certification or an accuracy/latency benchmark. The existing Docker recipe targets arm64 CPU; no multi-architecture image is included.

## Known limitations

One worker and one active inference request; overlapping requests receive 503. Request size and model context limits apply. Laya model capabilities come from upstream. Jev client compatibility has not been verified. The public replay is recorded output, not live inference.

## Attribution

Project code is MIT. Laya weights are Apache-2.0 from Convai Innovations. See MODEL_PROVENANCE.md for the pinned model revision, hashes, and license details.
