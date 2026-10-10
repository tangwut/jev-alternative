# SystemOne 小游戏

## 免安装业务回放

直接双击 `replay/index.html`，选择工单分流或 Agent 工具选择，再点击 Replay。页面内置真实模型的请求与响应记录，无需 Python、模型、API Key 或后端；不发送网络请求，不执行实时推理。记录版本和设备信息在页面中展示，录制的单次耗时不构成性能基准。

## 实时游戏

游戏固定使用 `english` 模型。单模型快速启动默认是 `multilingual`，不能直接用于这些游戏。首次准备时使用 `python scripts/setup_local.py --model english`；已有 `.env` 的用户请先妥善保存并移开配置，再准备 English，或手动配置已下载的 English 模型。

目录：

- `tetris/`：俄罗斯方块；SystemOne 每个方块选择一次落点。
- `snake/`：贪吃蛇；SystemOne 每移动一格选择一次方向。
- `config.example.js`：本地 API Key 的空白示例；复制为不提交的 `config.js`。

先在项目根目录启动现有 API：

```bash
python main.py
```

先复制 `frontend/config.example.js` 为 `frontend/config.js`，并将其中的空字符串改为本机 `.env` 里的 `LAYA_API_KEY`。等待 `/health` 就绪，然后直接双击 `frontend/tetris/index.html` 或 `frontend/snake/index.html`。页面直接请求 `http://127.0.0.1:8000/api/v1/systemone`，无需额外前端服务。`main.py` 允许本地 `file://` 页面所用的 `Origin: null` 跨域请求。`config.js` 仅供本地演示，不能保护公网密钥。

两个游戏都会先用本地规则生成安全候选，再由 SystemOne 做最终选择，页面显示候选、模型返回概率、原始请求与响应及移动记录。模型概率不能当成游戏胜率。模型无法响应时游戏暂停并显示错误。

测试：

```bash
node --test frontend/tetris/tests/core.test.mjs frontend/snake/tests/core.test.mjs frontend/replay/tests/replay.test.mjs
python -m pytest -q
```
