# 使用与上手

在仓库根执行以下命令。首次安装依赖需要网络，执行示例不需要 Key。默认环境 Python 3.12；最低验证目标为 Python 3.10。

```sh
uv sync --locked --python 3.12
uv run python examples/01-tool-agent/main.py --offline
uv run python examples/02-session-state/main.py --offline
uv run python examples/03-workflow-routing/main.py --text '你好？'
uv run python examples/04-human-in-the-loop/main.py --decision approve
uv run python examples/04-human-in-the-loop/main.py --decision reject
uv run pytest -q
```

| 示例 | 预期 | 最适合观察 |
| --- | --- | --- |
| [01 工具](../../examples/01-tool-agent/README.md) | 杭州：晴，24°C | FunctionCall 与真实返回闭环 |
| [02 状态](../../examples/02-session-state/README.md) | [1,2]、1、1 | 同会话累加、用户/会话隔离 |
| [03 路由](../../examples/03-workflow-routing/README.md) | visited 只有 question | 未选分支不执行 |
| [04 审批](../../examples/04-human-in-the-loop/README.md) | 批准一次、拒绝零次 | 真实暂停与公开参数恢复 |

阅读示例 main.py 是完整可运行入口。本文不复制长段 Python，避免与经过测试的代码分叉。四个示例彼此独立，无需启动 Web 服务；它们是执行机制演示，不是完整业务 Agent 应用。

下一步：[环境配置](environment.md) · [调试方法](debugging.md) · [生产决策](production-checklist.md) · [验证记录](../validation.md)
