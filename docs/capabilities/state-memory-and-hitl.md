# 状态、长期记忆与人工介入

## 连续对话先解决保存边界

SessionService 的职责是创建、读取会话并追加事件；State 的作用域前缀把会话、用户和应用数据区分开。选择数据库后端还需要连接、驱动、迁移与并发策略。DatabaseSessionService 检测过期版本时可以拒绝追加，应用需要处理重读或冲突；“有持久化后端”不等于任意并发写都成功。[数据库后端](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/sessions/database_session_service.py#L308)

[状态示例](../../examples/02-session-state/README.md)只验证 InMemory 后端的串行隔离。内存后端不跨进程保存；共享前缀也不能替代租户权限。完整写入路径见[状态与事件](../architecture/state-and-events.md)。

## Memory 与 Artifact 是另两类服务

Memory 提供 add_session_to_memory、add_events_to_memory、add_memory 与 search_memory 等接口，具体实现决定支持哪些写入方式以及检索行为。应明确什么内容值得保留、何时写入、如何检索和删除；仅把 memory_service 传给 Runner 并不能保证应用已经形成有效的记忆策略。[服务契约](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/memory/base_memory_service.py#L44)

Artifact 服务保存、读取内容并管理版本。模型需要文件时，应显式装载相应内容或引用。会话状态可以保存标识，但把大型二进制内容直接塞进 State 往往会增加序列化和历史开销。这个取舍是工程判断，需结合后端限制。[Artifact 接口](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/artifacts/base_artifact_service.py#L87)

## 两种“等用户”不要混为一谈

工具确认是在执行某个工具前请求批准；RequestInput 是工作流节点要求补充输入，可用于审批也可用于填信息。前者关联 ToolConfirmation 与 FunctionTool，后者关联 interrupt_id、response_schema 与节点恢复。二者最终都需要应用提供用户界面和身份校验。[工具确认](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/tools/function_tool.py#L389)、[RequestInput](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/events/request_input.py#L28)

[审批示例](../../examples/04-human-in-the-loop/README.md)通过公开 FunctionResponse 恢复，实际捕获的标识连接前后两轮。拒绝和无效决定都不能进入动作分支。示例只需核心包，不需要真实模型或托管服务。

## 没有被本地测试证明的事情

跨进程恢复必须保存会话及恢复所需执行信息；业务动作需要单独的幂等边界；长期记忆质量需要数据与评估；Artifact 生命周期要考虑保留和删除。当前示例没有覆盖数据库迁移、重复审批响应、进程崩溃或外部事务，不能据此承诺 exactly-once。
