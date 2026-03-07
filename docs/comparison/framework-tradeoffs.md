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
