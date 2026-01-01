# 证据索引

固定基线：**google-adk v2.10.0**，提交 `53b3706e04fab34d1d53808a5f62cfe9b025f893`。源码 version.py 为 2.10.0，与[发布标签](https://github.com/google/adk-python/releases/tag/v2.10.0)一致。以下 E-ADK 条目均对应此 SHA，核查日期统一为 **2026-09-29**。

源码说明实现；本地测试说明覆盖行为；滚动官方文档说明官方描述及配置；本仓库分析判断需给出条件。阅读资料不等于运行验证。

## E-ADK-001

- 主题：公开 API；类型：固定源码。
- 来源：[`__init__.py`](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/__init__.py#L26)。
- 验证：读取 lazy exports；限制：导出不保证所有实验能力稳定。

## E-ADK-002

- 主题：Agent 关系；类型：固定源码。
- 来源：[agents/llm_agent.py](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/agents/llm_agent.py#L267)。
- 验证：核对 LlmAgent 继承及第 1350 行 Agent 别名；限制：并非所有节点调用模型。

## E-ADK-003

- 主题：执行入口；类型：固定源码。
- 来源：[runners.py](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/runners.py#L1028)。
- 验证：读取 Runner 服务字段与 run_async；限制：节点路径与 live 分别分析。

## E-ADK-004

- 主题：图与节点；类型：固定源码。
- 来源：[workflow/_workflow.py](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/workflow/_workflow.py#L131)。
- 验证：核对 Workflow(BaseNode) 与图实现；限制：下划线文件用于定位，不是推荐导入路径。

## E-ADK-005

- 主题：事件；类型：固定源码。
- 来源：[events/event.py](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/events/event.py#L86)。
- 验证：阅读内容、动作与节点字段；限制：不同执行模式需结合调用链。

## E-ADK-006

- 主题：会话后端；类型：固定源码。
- 来源：[sessions/in_memory_session_service.py](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/sessions/in_memory_session_service.py#L74)。
- 验证：核对分层存储和第 333 行事件写回；限制：进程内实现，不证明多线程生产可用。

## E-ADK-007

- 主题：状态范围；类型：固定源码。
- 来源：[sessions/state.py](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/sessions/state.py#L72)。
- 验证：核对键值、delta 及三种前缀；限制：作用域不等于访问控制。
