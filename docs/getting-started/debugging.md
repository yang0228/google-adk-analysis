# 沿事件定位问题

先确认 Python 环境、ADK 版本和执行模式，再检查同一次调用的事件。不要仅根据最终文字判断工具是否成功。

| 表象 | 先观察什么 | 下一步 |
| --- | --- | --- |
| 工具没执行 | Event.get_function_calls() 是否有目标名与参数 | 检查工具声明、指令和模型请求 |
| 工具执行但回答不对 | FunctionResponse 内容及后续模型输入 | 区分工具数据错误与模型解释错误 |
| 状态不累加 | app_name/user_id/session_id，已保存 state | 比较 SessionService 的读取与 state_delta |
| 分支好像执行两遍 | actions.route、node_info.path、业务动作记录 | 区分节点重跑、重复输入与重复消费展示 |
| 审批后没有继续 | FunctionCall 的 id/name 与 invocation_id | 用匹配的 FunctionResponse 恢复原会话 |
| 有输出却还没结束 | partial、最终事件与生成器生命周期 | 消费完流并关闭 Runner |

[示例 01](../../examples/01-tool-agent/main.py)返回完整 Event 列表，适合加断点查看。不要直接把整份模型请求、凭证或私人会话输出到公共 Issue。需要复现时优先构造不含真实数据的最小请求。

Event(route=...) 是构造方式，读取字段是 actions.route；函数节点事件的 author 可能为 Workflow 名称，node_info.path 才能帮助定位具体节点。[源码解释](../architecture/request-lifecycle.md#用事件检验理解)

真实 Agent 应用可使用 ADK 的开发 Web UI 查看事件与 trace；本仓库的 main.py 是直接 Runner 演示入口，不假设可被 adk web 作为 root_agent 工程加载。上游开发 UI 的配置需按[官方文档](https://adk.dev/)完成，本项目未启动或暴露服务。
