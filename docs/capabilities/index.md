# 核心能力：从机制看边界

| 你要解决的问题 | 阅读入口 | 本地证据 |
| --- | --- | --- |
| 模型自治与确定流程怎样组合 | [Agent 与 Workflow](agents-and-workflows.md) | 路由示例 |
| 模型怎样调用本地或远程工具 | [工具、模型与协议](tools-and-models.md) | 工具示例 |
| 连续对话与审批怎样保存和继续 | [状态、记忆与人工介入](state-memory-and-hitl.md) | 状态、审批示例 |
| 怎样观察、评估和部署应用 | [评估、观测与部署](evaluation-observability-deployment.md) | 固定版本源码阅读，未部署 |

共同基线是 [v2.10.0](../references.md)。本仓库默认只安装核心依赖；带 eval、mcp、a2a、gcp 等标签的能力需要相应扩展或外部服务。不要把一张能力列表理解成安装核心包后无需配置便全部可用。
