# 参与贡献

## Contributing

Useful contributions include reproducible bug reports, installation feedback, client examples, evaluation data, and documentation improvements. See [the roadmap](docs/roadmap.md) for small tasks and acceptance evidence. Agree on scope in an issue before substantial changes. Maintainers can label well-defined starter tasks `good first issue`; contributors do not need to download models to run API tests.

Use Python 3.12 and Node.js 22 for the documented development environment. Describe the behavior change and validation in your PR. Never attach credentials, `.env`, private input data, or weights. A star is optional; it is not a prerequisite for help or contributions.

欢迎提交 Issue 和 Pull Request。提交问题时请提供复现步骤、预期结果、实际结果以及 Python/操作系统版本；不要附带 API Key、`.env` 或模型权重。

开发环境使用 Python 3.12 和 Node.js 22。Python 接口测试不需要下载模型：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-ci.txt
python -m pytest -q
node --test frontend/tetris/tests/core.test.mjs frontend/snake/tests/core.test.mjs frontend/replay/tests/replay.test.mjs
```

Windows 激活命令为 `.venv\Scripts\activate`。修改可观察行为时，请同时补充能复现问题或验证新行为的测试。Pull Request 请说明变更目的和验证结果。
