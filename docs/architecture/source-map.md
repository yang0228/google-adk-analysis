# 固定版本源码地图

以下全部链接指向 v2.10.0 的同一 SHA。内部路径帮助阅读源码；示例使用公开导入，不依赖这些下划线实现。

| 问题 | 入口 | 下一站 / 本地证据 |
| --- | --- | --- |
| 顶层可以导入什么 | [__init__.py:26](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/__init__.py#L26) | lazy exports |
| Agent 的继承和别名 | [llm_agent.py:267](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/agents/llm_agent.py#L267) | BaseAgent → BaseNode；文件末尾 Agent 别名 |
| 根节点怎么启动 | [runners.py:1028](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/runners.py#L1028) | run_async 分支；四个示例 |
| 调用上下文与队列从何而来 | [_node_runner_utils.py:69](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/workflow/_node_runner_utils.py#L69) | 解析恢复输入、启动根任务、消费队列 |
| 节点如何执行 | [_node_runner.py:115](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/workflow/_node_runner.py#L115) | 建立子 Context，调用 BaseNode.run |
| 节点通用契约 | [_base_node.py:44](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/workflow/_base_node.py#L44) | 输出、暂停和生命周期 |
| 图如何调度 | [_workflow.py:218](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/workflow/_workflow.py#L218) | ready nodes、完成事件、下游触发 |
| 调用级 Context | [invocation_context.py:113](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/agents/invocation_context.py#L113) | Session、服务与调用信息 |
| 节点级 Context | [context.py:115](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/agents/context.py#L115) | state、resume_inputs、run_node |
| Event 的便捷参数 | [event.py:164](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/events/event.py#L164) | state → actions.state_delta；route → actions.route |
| 动作差量与控制信号 | [event_actions.py:78](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/events/event_actions.py#L78) | State、Artifact、路由、移交 |
| 模型请求循环 | [base_llm_flow.py:389](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/flows/llm_flows/base_llm_flow.py#L389) | 预处理、模型、后处理、工具 |
| 模型扩展接口 | [base_llm.py:132](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/models/base_llm.py#L132) | generate_content_async；示例 01/02 替身 |
| Python 工具调用 | [function_tool.py:357](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/tools/function_tool.py#L357) | 参数解析与函数执行；示例 01/02 |
| 事件何时落入服务 | [runners.py:750](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/runners.py#L750) | 非 partial 事件保存后 yield |
| Session 后端如何合并 | [in_memory_session_service.py:333](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/sessions/in_memory_session_service.py#L333) | app/user/session 差量；示例 02 |
| 暂停信号 | [request_input.py:28](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/events/request_input.py#L28) | 自动生成 interrupt_id、响应 schema |
| 恢复响应怎样解包 | [_rehydration_utils.py:100](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/workflow/utils/_rehydration_utils.py#L100) | 仅 result 的字典解包；示例 04 |
| 实时入口 | [runners.py:1579](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/runners.py#L1579) | run_live；本仓库未实测 |

建议用本地示例输出对照[请求时序](request-lifecycle.md)，不要从文件名猜测 API 稳定性。[统一证据说明](../references.md)
