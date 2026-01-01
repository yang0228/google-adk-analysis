# 术语与易混点

| 术语 | 含义 | 不应混同 |
| --- | --- | --- |
| Agent / LlmAgent | 模型驱动的节点，声明指令和工具 | 用户会话实例 |
| BaseNode | 节点执行契约 | 仅 LLM 节点 |
| Workflow | 节点与边组成的图 | 外层 Python if/else |
| Runner | 根节点入口及服务协调者 | 全局用户状态 |
| NodeRunner | 内部节点执行器 | 应用应直接依赖的公共入口 |
| InvocationContext | 一次调用的上下文 | 长期存储 |
| Context | 当前节点的运行上下文 | 无边界的全局对象 |
| Event | 内容、动作与执行信息载体 | 最终文字回答 |
| Session | app/user/session 下的事件与状态 | 身份认证系统 |
| State | 当前值及待提交差量 | 任意共享字典 |
| Memory | 跨会话存取与检索服务 | Session 的别名 |
| Artifact | 内容对象和版本保存服务 | 模型必然可见的内容 |
| RequestInput | 节点请求输入的暂停信号 | 审批 UI 和权限控制 |
| MCP | 工具与资源协议 | Agent 间任务委托 |
| A2A | Agent 间通信协议 | 本地函数工具接口 |

`app:`、`user:`、`temp:` 是 State 的作用域前缀，无前缀键通常属于当前会话。它们表达存储范围，不能替代访问控制。[前缀定义](../references.md#e-adk-007)

术语以[固定版本证据](../references.md)为准，首次阅读请配合[概览](index.md)。
