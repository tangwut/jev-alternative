import hashlib
import importlib.util
from pathlib import Path

import pytest
from dotenv import dotenv_values


def load_setup():
    path = Path(__file__).parents[1] / "scripts/setup_local.py"
    assert path.is_file(), "Missing single-model setup tool"
    spec = importlib.util.spec_from_file_location("setup_local", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def checkpoint(module, root, model="multilingual"):
    directory = root if model == "english" else root / model
    for name in module.REQUIRED_FILES:
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"test checkpoint")
    module.WEIGHT_SHA256[model] = hashlib.sha256(b"test checkpoint").hexdigest()


def test_existing_checkpoint_creates_private_single_model_configuration(tmp_path):
    module = load_setup()
    root = tmp_path / "model cache"
    checkpoint(module, root)
    config = module.prepare(tmp_path, model_root=root)
    values = dotenv_values(config)
    assert values["LAYA_MODELS"] == "multilingual"
    assert values["LAYA_MODEL_ROOT"] == str(root.resolve())
    assert values["LAYA_DEVICE"] == "cpu"
    assert values["LAYA_HOST"] == "127.0.0.1"
    assert len(values["LAYA_API_KEY"]) >= 32
    assert config.stat().st_mode & 0o077 == 0


def test_generated_configuration_can_be_used_as_a_docker_env_file(tmp_path):
    module = load_setup()
    root = tmp_path / "model cache"
    checkpoint(module, root)
    config = module.prepare(tmp_path, model_root=root)
    dotenv = dotenv_values(config)
    # Docker's --env-file preserves quotes literally. The documented container
    # command overrides the host-only model root, but uses all other values.
    docker = dict(line.split("=", 1) for line in config.read_text().splitlines() if line and not line.startswith("#"))
    for key in ("LAYA_MODELS", "LAYA_DEVICE", "LAYA_HOST", "LAYA_PORT", "LAYA_API_KEY"):
        assert docker[key] == dotenv[key], f"Docker and dotenv disagree on {key}"


def test_existing_configuration_is_preserved_before_download(tmp_path, monkeypatch):
    module = load_setup()
    config = tmp_path / ".env"
    config.write_text("existing configuration")
    monkeypatch.setattr(module, "fetch_snapshot", lambda model: pytest.fail("must not download"))
    with pytest.raises(FileExistsError):
        module.prepare(tmp_path)
    assert config.read_text() == "existing configuration"


def test_preparation_downloads_only_selected_model(tmp_path, monkeypatch):
    module = load_setup()
    root = tmp_path / "snapshot"
    checkpoint(module, root)
    calls = []
    monkeypatch.setattr(module, "fetch_snapshot", lambda model: calls.append(model) or root)
    module.prepare(tmp_path)
    assert calls == ["multilingual"]


def test_incomplete_or_invalid_weights_leave_no_configuration(tmp_path):
    module = load_setup()
    root = tmp_path / "snapshot"
    with pytest.raises(ValueError, match="Incomplete"):
        module.prepare(tmp_path, model_root=root)
    assert not (tmp_path / ".env").exists()
    checkpoint(module, root)
    (root / "multilingual/model.safetensors").write_bytes(b"version https://git-lfs.github.com/spec/v1")
    with pytest.raises(ValueError, match="checksum"):
        module.prepare(tmp_path, model_root=root)
    assert not (tmp_path / ".env").exists()
