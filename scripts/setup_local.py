"""Prepare one pinned Laya model and a private local .env; never overwrite it."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets

REPOSITORY = "convaiinnovations/laya"
REVISION = "aa8c91ca088ec597df95a0d1c76b3063cb2ae5e8"
WEIGHT_SHA256 = {
    "english": "891102d372688fc2a094dac56a384bc537b87c63f21f9f3dac0be2b7cbc8d86c",
    "multilingual": "9d628fd971b700382ac6f65920a86f149777b2e748e0c955fb3b19695aa8f204",
    "typed-decisions": "4fa56de72383a9d3efa9cfa78955733c81b9fc8067a587ca4beb82c78107a24e",
}
REQUIRED_FILES = ("rl_agent_config.json", "model.safetensors", "tokenizer/tokenizer.json",
                  "tokenizer/tokenizer_config.json", "encoder/config.json")


def fetch_snapshot(model: str) -> Path:
    from huggingface_hub import snapshot_download

    patterns = (["rl_agent_config.json", "model.safetensors", "tokenizer/*", "encoder/*"]
                if model == "english" else [f"{model}/*"])
    return Path(snapshot_download(repo_id=REPOSITORY, revision=REVISION,
                                  allow_patterns=[*patterns, "LICENSE", "README.md"]))


def prepare(project_root: Path, *, model="multilingual", device="cpu", model_root=None) -> Path:
    if model not in WEIGHT_SHA256:
        raise ValueError("Unsupported model")
    if device not in ("cpu", "cuda", "mps"):
        raise ValueError("Unsupported device")
    config = project_root / ".env"
    if config.exists() or config.is_symlink():
        raise FileExistsError(".env already exists; keep it and edit it manually, or move it aside first")
    root = Path(model_root if model_root is not None else fetch_snapshot(model)).expanduser().resolve()
    directory = root if model == "english" else root / model
    missing = [name for name in REQUIRED_FILES if not (directory / name).is_file()]
    if missing:
        raise ValueError(f"Incomplete {model} checkpoint: {', '.join(missing)}")
    with (directory / "model.safetensors").open("rb") as weights:
        digest = hashlib.file_digest(weights, "sha256").hexdigest()
    if digest != WEIGHT_SHA256[model]:
        raise ValueError("Weight checksum does not match MODEL_PROVENANCE.md; check download or Git LFS")
    values = {
        "LAYA_MODEL_ROOT": str(root), "LAYA_MODELS": model, "LAYA_DEVICE": device,
        "LAYA_HOST": "127.0.0.1", "LAYA_PORT": "8000", "LAYA_API_KEY": secrets.token_urlsafe(32),
    }
    # Exclusive creation protects existing configuration even if another setup runs concurrently.
    descriptor = os.open(config, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as output:
        output.write("# Generated local configuration. Do not commit this file.\n")
        for key, value in values.items():
            # Quote only the host path for dotenv escaping. The container recipe
            # overrides that path; Docker must see literal, unquoted settings/key.
            encoded = json.dumps(value, ensure_ascii=False) if key == "LAYA_MODEL_ROOT" else value
            output.write(f"{key}={encoded}\n")
    return config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", choices=tuple(WEIGHT_SHA256), default="multilingual")
    parser.add_argument("--device", choices=("cpu", "cuda", "mps"), default="cpu")
    parser.add_argument("--model-root", type=Path, help="Existing snapshot root or project models/ directory")
    args = parser.parse_args()
    try:
        config = prepare(Path(__file__).resolve().parents[1], model=args.model,
                         device=args.device, model_root=args.model_root)
    except (OSError, ValueError, ImportError) as error:
        parser.exit(1, f"Setup failed: {error}\n")
    print(f"Created {config.name} for {args.model} on {args.device}; the API key stays in that file.")
    print("Start: python main.py")
    print(f"Then: python example_client.py --model {args.model}")


if __name__ == "__main__":
    main()
