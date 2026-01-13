# 01 · 一次真实工具调用

在仓库根运行：

```sh
uv sync --locked --python 3.12
uv run python examples/01-tool-agent/main.py --offline
```

预期输出：`杭州：晴，24°C`。完整可运行代码：[main.py](main.py)。

OfflineWeatherModel 先生成 get_weather 的 FunctionCall；真实 ADK Runner 调用 Python 工具，把 FunctionResponse 放回下一次模型请求；替身读取这个实际结果生成文字。没有绕过 Runner 直接调用工具。天气本身是固定演示数据。

run_demo 返回全部 Event、工具请求参数与最终文字；[测试](../../tests/test_tool_agent.py)同时检查三者，并禁止互联网 socket。该测试证明本地调用闭环，不证明真实模型一定选择正确工具。

真实模型模式用 `--live`，必须先在进程环境中设置 GOOGLE_API_KEY 和 ADK_MODEL；缺失配置退出码为 2。.env.example 不会自动加载。在线调用可能产生费用，尚未执行。两个模式均使用同一个演示天气工具。
