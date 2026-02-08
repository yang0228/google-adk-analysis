# 04 · 暂停、批准与拒绝

在仓库根运行：

```sh
uv run python examples/04-human-in-the-loop/main.py --decision approve
uv run python examples/04-human-in-the-loop/main.py --decision reject
```

两次都先暂停。批准返回 executed_actions=["record_approval"]；拒绝返回空列表。动作仅是进程内列表追加，不发送消息、不写业务数据库。完整可运行代码：[main.py](main.py)。

第一轮运行到 RequestInput(response_schema=str)，消费完事件流后捕获 long_running_tool_ids 对应的真实 FunctionCall。第二轮使用相同 session、捕获的 invocation_id、call.id 和 call.name，把 FunctionResponse(response={"result": decision}) 交回公开 Runner.run_async。固定版本会解包 result，作为等待节点的输出交给后续路由；不导入内部恢复辅助函数。

[测试](../../tests/test_human_in_the_loop.py)验证真实暂停时没有动作、批准一次、拒绝零次、无效决定抛错。这里演示同一进程内的暂停恢复，没有审批 UI 或审批人鉴权，也没有验证进程崩溃恢复、重复响应或外部副作用 exactly-once。

参考固定版本 [RequestInput](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/events/request_input.py#L28)、[响应解包](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/workflow/utils/_rehydration_utils.py#L100)和[上游函数节点测试](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/tests/unittests/workflow/test_function_node.py#L433)。
