# 02 · 复用 Runner 后的状态边界

在仓库根运行：

```sh
uv run python examples/02-session-state/main.py --offline
```

输出字段应为 same_session_values=[1,2]、other_session_value=1、other_user_value=1。完整可运行代码：[main.py](main.py)。

一个 Agent、一个 Runner、一个 InMemorySessionService 处理四次调用。工具从 ToolContext.state 读取并写入 counter，每轮结束后重新从服务取得保存值。同用户同会话累加，另一会话与另一用户的同名会话各从 1 开始。[测试](../../tests/test_session_state.py)检查这些值。

无前缀 counter 属于 Session。`user:` 和 `app:` 键另有共享范围，`temp:` 表示调用期临时状态；此例不验证它们，也不构成多租户授权测试。不要把用户状态保存在共享 Agent 属性中。

默认替身仅安排工具调用和读取结果，真实状态写入仍由 ADK 执行。`--live` 要求进程环境中的 GOOGLE_API_KEY 与 ADK_MODEL，缺失返回 2；不自动加载 .env。真实模型可能漏调用或重复调用，在线路径尚未验证。InMemory 数据不跨进程持久化，不适合据此推断生产并发保证。
