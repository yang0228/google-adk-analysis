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
