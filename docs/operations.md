# Running the local API

[Project overview](../README.md) · [中文完整说明](../README.zh-CN.md)

## Platforms

The documented runtime is Python 3.12. CPU is the default; runtime compatibility and performance must be checked on your hardware. Do not interpret passing API unit tests as validation of every OS/device combination.

macOS/Linux commands are in the main README. Windows PowerShell:

```powershell
$env:GIT_LFS_SKIP_SMUDGE = "1"
git clone https://github.com/tangwut/jev-alternative.git
cd jev-alternative
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/setup_local.py
.\.venv\Scripts\python.exe main.py
```

Use a second PowerShell window to call `.\.venv\Scripts\python.exe example_client.py --scenario support --model multilingual` from the project directory. These commands avoid needing to change PowerShell's script execution policy.

## Model preparation

`python scripts/setup_local.py` downloads only multilingual files from the revision in MODEL_PROVENANCE.md into the Hugging Face cache and stores the snapshot's absolute path in `.env`. This is the only setup step that downloads a model. The running service uses local files.

- `--model english`: use English for live Tetris/Snake demos.
- `--model typed-decisions`: load the typed-decisions checkpoint.
- `--device cpu|cuda|mps`: choose the requested device.
- `--model-root PATH`: use an existing **snapshot root** or the complete project `models/` directory, without downloading.

The tool validates required files and the selected weight's pinned SHA-256 before creating `.env`. It creates a random Bearer key without printing it. POSIX permissions are set to owner read/write only; Windows uses the directory's inherited ACLs. Existing `.env` files are preserved. To prepare a different model, keep a backup of your configuration and move `.env` aside, or configure a separately downloaded checkpoint manually. Do not share the backup or commit it.

## Manual configuration and multiple models

For the original bundled models, install Git LFS and run `git lfs pull`. All three weights total about 2.2 GB. Copy `.env.example` to `.env`, generate a key with `python -c 'import secrets; print(secrets.token_urlsafe(32))'`, and set the desired configuration:

| Variable | Meaning |
| --- | --- |
| `LAYA_MODEL_ROOT` | Defaults to `models/`; relative paths resolve from the project directory |
| `LAYA_MODELS` | Comma-separated preloaded models; existing default is `english,multilingual,typed-decisions` |
| `LAYA_DEVICE` | Requested device, default CPU |
| `LAYA_HOST`, `LAYA_PORT` | Listener, default `127.0.0.1:8000` |
| `LAYA_API_KEY` | Required Bearer secret |

Process environment variables override `.env`. A snapshot root uses English files at its root and other variants in `multilingual/` and `typed-decisions/`. A Hugging Face cache root resolves `refs/main` to `snapshots/<revision>`; a fixed snapshot path is preferable for reproducibility. Missing files cause startup failure, never an online fallback download. Laya can update tokenizer configuration for compatibility, so the checkpoint needs write permission.

Run `python main.py` with **one worker and no `--reload`**. Multiple workers duplicate model memory. Stop with Ctrl+C; restart reloads the models. Use systemd, launchd, or a container for process supervision.

## API

| Endpoint | Authentication | Purpose |
| --- | --- | --- |
| `GET /health` | None | Returns ready state or 503 |
| `GET /api/v1/models` | Bearer | Loaded models and requested device |
| `POST /api/v1/systemone` | Bearer | Inference |
| `GET /docs` | None for page | Interactive API reference; inference still requires Bearer authentication |

`state` accepts a string, object, or list. `questions` must contain 1–20 questions with `type` and `instructions`. `choice` criteria are unique string labels or a label-to-description mapping. `score` criteria are an ordered list. `noul` criteria may be omitted or supplied as a true/false description mapping.

Pass `model` explicitly when using a single-model setup. Without it, language routing can select a model that has not been preloaded. `typed-decisions` always needs an explicit model selection.

Errors: **401** for invalid keys; **413** for bodies over 64 KiB including chunked requests; **422** for invalid questions, unknown fields, or unconfigured models; **503** for busy/unready models; **500** for internal inference failures with sanitized details. Busy responses include `Retry-After: 1`; use randomized backoff. There is no dynamic batching across requests.

## Deployment

For LAN use, set an appropriate listening address and call the **server's IP**. Do not use `0.0.0.0` as a client destination or the client's own `127.0.0.1`.

For internet access, add an HTTPS reverse proxy, firewall rules, rate limiting, and request read timeouts. The project creates neither a public endpoint nor an OS service automatically. Local `file://` game pages are allowed through `Origin: null` CORS; this is a local-demo setting, not a general public hosting configuration. Browser-side `frontend/config.js` cannot protect a public secret.

### Docker: existing arm64 CPU recipe

The existing Dockerfile bundles all models. Run `git lfs pull` before building; LFS pointer files are insufficient. This path is separate from the one-model cache setup, and is not a published multi-architecture image.

```bash
docker build --platform linux/arm64 -t systemone:local .
docker run --rm --name systemone --env-file .env -e LAYA_MODEL_ROOT=/app/models -e LAYA_HOST=0.0.0.0 -e LAYA_PORT=8000 -p 8001:8000 systemone:local
```

The explicit overrides replace the host cache path and local-only listener in `.env`, and keep the container port aligned with the mapping. Wait for preloading, then check `http://127.0.0.1:8001/health`. Allocate enough RAM for the selected model set. Authenticate API calls with the same Bearer key.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Setup refuses to proceed | Keep/edit the existing `.env`; the tool intentionally does not overwrite it |
| Weight checksum mismatch | Check the pinned revision and whether weights are Git LFS pointers |
| Incomplete checkpoint | Supply the snapshot **root**, not the multilingual subdirectory |
| Setup download fails | Check internet access, disk space, and Hugging Face availability; retry uses its cache |
| Startup rejects API key | Configure `LAYA_API_KEY`; check overriding process variables |
| 422 selected model not enabled | Pass `--model multilingual` in the quick-start client |
| Slow startup or high RAM | Load one model; check actual device and fallback logs |
| Game calls return 422 | The games require the English model; see frontend/README.md |
