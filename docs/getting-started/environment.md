# 环境与配置

## 固定依赖

pyproject.toml 固定 google-adk==2.10.0，uv.lock 固定解析结果。运行 `uv sync --locked --python 3.12`，再用 `uv run` 调用项目环境。不要无意间混用机器上其他版本的 adk 命令。若更新 ADK，需一起更新源码 SHA、证据和示例验证结果。

[uv 安装文档](https://docs.astral.sh/uv/getting-started/installation/)是工具安装入口。Python 3.10 使用独立环境，避免覆盖默认环境：

```sh
UV_PROJECT_ENVIRONMENT=.venv-310 uv sync --locked --python 3.10
UV_PROJECT_ENVIRONMENT=.venv-310 uv run pytest -q
```

Markdown 和图表检查使用 Node.js 22。普通阅读和运行 Python 示例不需要 Node；文档维护时安装 package-lock.json 中的工具。首次依赖安装及 Mermaid 浏览器下载需要网络。

## 默认离线

示例 01/02 的模型替身只返回预先安排的响应，真实 ADK 负责执行工具、追加事件和更新状态。示例 03/04 是函数工作流。pytest-socket 禁止互联网 socket，保留 asyncio 使用的 Unix socket。

你可能看到 ADK 实验功能提示和替身缺少 token usage 的日志，它们不是测试失败。依赖导入时的 IPv6 探测也可能被 socket 检查阻止并警告，具体来源见[验证记录](../validation.md)。

## 可选真实模型

只有示例 01/02 提供 `--live`。它们从进程环境读取 GOOGLE_API_KEY 和 ADK_MODEL；任何一项为空，返回退出码 2，错误只显示变量名。Key 请通过本地环境或密码管理器设置，不要提交到仓库。

[.env.example](../../.env.example)只是说明模板，脚本不会自动读取 .env。可在 shell 显式 export 变量；下面的 Key 是占位符，不是有效凭证，命令仅供手动配置参考，**未作为验证步骤执行**：

```sh
export GOOGLE_API_KEY='replace-with-your-local-key'
export GOOGLE_GENAI_USE_VERTEXAI=FALSE
export ADK_MODEL='gemini-3.8-flash'
uv run python examples/01-tool-agent/main.py --live
```

模型 ID 按 2026-09-29 的 [Google 模型目录](https://ai.google.dev/gemini-api/docs/models)核对。文档可用不保证你的账号、区域或配额可用；在线调用可能计费。这里选择 Gemini Developer API 路径，Vertex AI 使用不同凭证和项目配置，未在示例中验证。

真实模型可能省略工具、改变参数或多次调用；同一演示天气工具仍返回固定数据。不要把确定性测试的精确回答要求直接用于在线输出。
