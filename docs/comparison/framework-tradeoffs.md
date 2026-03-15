# 五个框架，八个维度

## 比较口径与版本

**内置**：SDK 自带接口，仍可能需要外部模型与配置。**扩展**：另装依赖或连接专用引擎。**托管**：平台服务，不等于开源包自带。**应用**：由应用实现或接入。本表不把“尚未核实”写成“不支持”。

| 项目 | 固定版本 | 提交 | 发布日期（UTC） |
| --- | --- | --- | --- |
| ADK | v2.10.0 | 53b3706e04fab34d1d53808a5f62cfe9b025f893 | 2026-09-25 |
| LangGraph | [1.2.12](https://github.com/langchain-ai/langgraph/releases/tag/1.2.12) | 49cce0ca852be4cfb567a1cbe0e511ff325a1682 | 2026-09-21 |
| OpenAI Agents SDK | [v0.22.3](https://github.com/openai/openai-agents-python/releases/tag/v0.22.3) | fdf21db62c303a3db54b0dfbee82de2141fa2799 | 2026-09-17 |
| PydanticAI | [v2.51.0](https://github.com/pydantic/pydantic-ai/releases/tag/v2.51.0) | 39328d5b0d4cce94d513b6afcd2b3191bd5708d5 | 2026-09-25 |
| CrewAI | [1.15.22](https://github.com/crewAIInc/crewAI/releases/tag/1.15.22) | 7a01af27912c2b142d8bac70d1894343f8b91bd1 | 2026-09-16 |

核查日期为 2026-09-29。LangGraph 取主包 1.2.12，不能使用仓库 latest API 返回的 CLI 标签代替。CrewAI 注释标签已解析到实际 commit。滚动站点用于交叉核查，下面固定文档是版本依据；并未为四个竞品安装和运行示例。

## 统一维度表

为控制宽度，每格只写机制与必要条件。列标题链接到本页的固定来源，每个来源组覆盖对应列；更细的 ADK 证据在专题文档。

| 维度 | [ADK](#adk-证据) | [LangGraph](#langgraph-证据) | [OpenAI Agents SDK](#openai-agents-sdk-证据) | [PydanticAI](#pydanticai-证据) | [CrewAI](#crewai-证据) |
| --- | --- | --- | --- | --- | --- |
| 核心编排 | 内置 Agent、Workflow、函数节点与 Runner | 内置 StateGraph、节点、边和状态归并 | 内置 Agent/Runner、handoff；应用代码组织流程 | 内置 Agent 与类型化依赖；图编排为 pydantic-graph 组件 | 内置角色 Agent/Task/Crew 与事件驱动 Flow |
| 模型与工具 | 内置函数工具、Gemini；扩展 MCP、OpenAI、A2A 等 | 应用节点调用模型工具；可选 LangChain 组件 | 内置函数、MCP、OpenAI 模型接口；其他提供商需适配核验 | 内置工具和模型抽象；提供商及 MCP 按 extra 配置 | 内置 LLM 与工具接口；工具包、MCP 及提供商按集成配置 |
| 状态与恢复 | 内置 Session/State、节点恢复；持久后端另配 | 内置 checkpoint 契约；扩展数据库 saver，按 thread 恢复 | 内置 Session 历史与 RunState；持久化和恢复需应用接线 | 历史持久化与 durable execution 分开；扩展 Temporal 等引擎 | 内置状态及 checkpoint 配置；需选择保存策略与后端 |
| 类型与结构化输出 | 内置 input/output schema；组合能力受模型约束 | 内置状态及输入输出 schema；模型输出校验在节点/集成层 | 内置 output_type 和函数参数 schema；取决于模型能力 | 内置 output_type、Pydantic 校验及依赖类型 | 内置 Task output_pydantic/output_json；需配置任务与模型 |
| 人工介入 | 内置工具确认和 RequestInput；应用审批 UI/身份 | 内置 interrupt + Command；需 checkpointer，节点从头重跑 | 内置 needs_approval、interruptions、RunState 批准/拒绝 | 内置 deferred tools；应用提供审批/外部结果 | 内置 human_input、Flow human_feedback；应用选择反馈渠道 |
| 观测与评估 | 内置事件、插件、OTel；扩展 eval、导出后端 | 内置流和状态观察；LangSmith 观测评估属平台集成 | 内置 tracing；平台 dashboard/评估另计，可换 processor | 内置仪器化接口；扩展 Pydantic Evals，Logfire 为平台 | 内置事件监听和 crew test；AMP 等平台另计 |
| 实时与多模态 | 内置 run_live；需兼容模型、连接和媒体端 | 内置流式图输出；双向语音端到端为应用/集成，未核实等价 SDK API | 内置 RealtimeAgent/Runner；Python 服务端传输，需 Realtime 模型 | 内置 realtime 接口；提供商 extra 与应用音频传输 | 内置多模态 Agent 配置；双向语音等价路径尚未核实 |
| 部署与依赖 | 应用可自托管；扩展 GCP 部署入口 | 应用可自托管；LangSmith Deployment 为平台 | 应用运行 Python SDK；模型、工具和 trace 服务另配 | 应用可自托管；durable 引擎和观测平台单独部署/接入 | 应用运行 Crew/Flow；AMP 为独立平台选项 |

## ADK 证据

[公开对象与调用链](../architecture/source-map.md)、[工具和模型依赖](../capabilities/tools-and-models.md)、[状态与恢复](../architecture/state-and-events.md)、[评估、实时和部署](../capabilities/evaluation-observability-deployment.md)。四个示例只验证离线控制流和内存后端，不替任何生产能力作背书。

## LangGraph 证据

[StateGraph](https://github.com/langchain-ai/langgraph/blob/49cce0ca852be4cfb567a1cbe0e511ff325a1682/libs/langgraph/langgraph/graph/state.py#L131) 定义状态、输入输出 schema 与归并；[interrupt](https://github.com/langchain-ai/langgraph/blob/49cce0ca852be4cfb567a1cbe0e511ff325a1682/libs/langgraph/langgraph/types.py#L887) 明确需要 checkpointer，并从节点开头重执行；[checkpoint 契约](https://github.com/langchain-ai/langgraph/blob/49cce0ca852be4cfb567a1cbe0e511ff325a1682/libs/checkpoint/README.md)与[Postgres saver](https://github.com/langchain-ai/langgraph/blob/49cce0ca852be4cfb567a1cbe0e511ff325a1682/libs/checkpoint-postgres/README.md)区分接口和后端。[项目 README](https://github.com/langchain-ai/langgraph/blob/49cce0ca852be4cfb567a1cbe0e511ff325a1682/README.md)介绍自托管代码与 LangSmith 集成；[官方架构定位](https://docs.langchain.com/oss/python/langgraph/overview)和[持久化文档](https://docs.langchain.com/oss/python/langgraph/persistence)于核查日读取。模型/工具接入与图调度分层是选型重点；未核实音频 API 不意味着应用不能集成语音。

## OpenAI Agents SDK 证据

[Agent 配置](https://github.com/openai/openai-agents-python/blob/fdf21db62c303a3db54b0dfbee82de2141fa2799/docs/agents.md)、[模型适配](https://github.com/openai/openai-agents-python/blob/fdf21db62c303a3db54b0dfbee82de2141fa2799/docs/models/index.md)、[工具](https://github.com/openai/openai-agents-python/blob/fdf21db62c303a3db54b0dfbee82de2141fa2799/docs/tools.md)覆盖运行抽象与类型输出；[Session](https://github.com/openai/openai-agents-python/blob/fdf21db62c303a3db54b0dfbee82de2141fa2799/docs/sessions/index.md)与[HITL/RunState](https://github.com/openai/openai-agents-python/blob/fdf21db62c303a3db54b0dfbee82de2141fa2799/docs/human_in_the_loop.md)区分历史管理与暂停恢复。[Tracing](https://github.com/openai/openai-agents-python/blob/fdf21db62c303a3db54b0dfbee82de2141fa2799/docs/tracing.md)允许替换处理器，不能把平台 dashboard 当作 SDK 内存对象；[Realtime](https://github.com/openai/openai-agents-python/blob/fdf21db62c303a3db54b0dfbee82de2141fa2799/docs/realtime/guide.md)描述 Python 服务端连接，浏览器 WebRTC 不属于这套 Python SDK 的传输接口。滚动资料：[运行 Agent](https://developers.openai.com/api/docs/guides/agents/running-agents)、[集成与观测](https://developers.openai.com/api/docs/guides/agents/integrations-observability)。

## PydanticAI 证据

[项目概览](https://github.com/pydantic/pydantic-ai/blob/39328d5b0d4cce94d513b6afcd2b3191bd5708d5/docs/index.md)、[输出类型](https://github.com/pydantic/pydantic-ai/blob/39328d5b0d4cce94d513b6afcd2b3191bd5708d5/docs/output.md)、[延迟工具](https://github.com/pydantic/pydantic-ai/blob/39328d5b0d4cce94d513b6afcd2b3191bd5708d5/docs/deferred-tools.md)覆盖类型约束及人工介入；[历史持久化](https://github.com/pydantic/pydantic-ai/blob/39328d5b0d4cce94d513b6afcd2b3191bd5708d5/docs/persistence.md)与[持久执行](https://github.com/pydantic/pydantic-ai/blob/39328d5b0d4cce94d513b6afcd2b3191bd5708d5/docs/durable_execution/overview.md)明确区分保存会话和跨故障维持一个 run。[Realtime](https://github.com/pydantic/pydantic-ai/blob/39328d5b0d4cce94d513b6afcd2b3191bd5708d5/docs/realtime/overview.md)已有多提供商语音接口；[观测](https://github.com/pydantic/pydantic-ai/blob/39328d5b0d4cce94d513b6afcd2b3191bd5708d5/docs/logfire.md)说明可选仪器化和平台关系。不能再把它简化成“只有结构化输出的小框架”。[滚动官方概览](https://pydantic.dev/docs/ai/overview/)另于核查日读取。

## CrewAI 证据

固定目录 docs/v1.15.22/en 中的 [Flows](https://github.com/crewAIInc/crewAI/blob/7a01af27912c2b142d8bac70d1894343f8b91bd1/docs/v1.15.22/en/concepts/flows.mdx)、[Tasks](https://github.com/crewAIInc/crewAI/blob/7a01af27912c2b142d8bac70d1894343f8b91bd1/docs/v1.15.22/en/concepts/tasks.mdx)、[LLMs](https://github.com/crewAIInc/crewAI/blob/7a01af27912c2b142d8bac70d1894343f8b91bd1/docs/v1.15.22/en/concepts/llms.mdx)覆盖编排、输出和模型。[检查点](https://github.com/crewAIInc/crewAI/blob/7a01af27912c2b142d8bac70d1894343f8b91bd1/docs/v1.15.22/en/concepts/checkpointing.mdx)与[人工反馈](https://github.com/crewAIInc/crewAI/blob/7a01af27912c2b142d8bac70d1894343f8b91bd1/docs/v1.15.22/en/learn/human-feedback-in-flows.mdx)已有暂停恢复相关机制；[多模态](https://github.com/crewAIInc/crewAI/blob/7a01af27912c2b142d8bac70d1894343f8b91bd1/docs/v1.15.22/en/learn/multimodal-agents.mdx)不应等同于低延迟双向语音。[事件监听](https://github.com/crewAIInc/crewAI/blob/7a01af27912c2b142d8bac70d1894343f8b91bd1/docs/v1.15.22/en/concepts/event-listener.mdx)和[测试评估](https://github.com/crewAIInc/crewAI/blob/7a01af27912c2b142d8bac70d1894343f8b91bd1/docs/v1.15.22/en/concepts/testing.mdx)提供观测入口。[官方介绍](https://docs.crewai.com/v1.15.22/en/introduction)区分开源组件与 AMP。

## 三个场景的取舍

**现有 Python 应用中的结构化工具任务。** 如果重点是类型、依赖注入和把结果交回现有业务函数，可先比较 PydanticAI 与 OpenAI Agents SDK 的小型实现；若还需要 ADK 的 Session、工具上下文或 Google 集成，ADK 也适合做同题验证。比较接入代码量、失败处理和可观测性，不以框架名字判断成本。

**需要人工审批的有状态流程。** 若流程图和 checkpoint 是核心，优先验证 LangGraph 的状态归并、interrupt 重跑边界；ADK 适合验证 Agent 与函数混合图和 RequestInput。已有 Temporal 等基础设施时，PydanticAI 的引擎集成值得纳入；角色任务型工作负载也可测试 CrewAI Flow。所有候选都应实测拒绝、重复响应、重启及外部动作幂等。

**已有 Google Cloud 的 Agent 应用。** ADK 的模型、服务和部署入口可能减少自行接线，前提是 IAM、存储区域、预算和现有运维流程兼容。用一次真实部署验证这个判断后再推广。其他框架也可运行在 Google Cloud，平台适配便利不能推导为排他部署能力。

## ADK 特别在哪

基于以上事实，本仓库的判断是：ADK 把交互式 Agent、显式图调度、统一事件、会话服务和 Google 生态入口放在同一工具包中，适合沿一条执行链理解和调试。代价是运行模式、上下文和服务边界较多。它的特色是组合方式；HITL、持久化、多模态或类型输出各自都不足以证明“独有”。
