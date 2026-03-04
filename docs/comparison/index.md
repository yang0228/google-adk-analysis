# 特性与框架比较

ADK 的辨识度来自一组设计的组合：Agent 与函数节点共享节点契约、事件贯穿执行和会话、Workflow 与交互式 Agent 共存，以及 Google 服务集成。单独的工具调用、HITL、类型输出或持久化并非它独有。[ADK 机制](../architecture/index.md)

[统一比较表](framework-tradeoffs.md)覆盖 ADK、LangGraph、OpenAI Agents SDK、PydanticAI、CrewAI。每格区分内置接口、扩展集成、托管平台与应用实现；没有做跨框架性能基准，不给星级排名。

源码与文档核查日期：**2026-09-29**。ADK 示例经过本地运行，其余项目只检查固定版本官方资料，证据强度并不相同。选型结论是条件判断，不是“支持项最多就最好”。
