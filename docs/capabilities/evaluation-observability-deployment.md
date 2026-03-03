# 评估、观测、实时与部署

## 评估不是多跑几次单元测试

AgentEvaluator 根据 EvalSet、配置指标和重复次数执行评估；它关注模型与工具轨迹是否满足预期。v2.10.0 的预置指标还包含工具调用数、模型调用数、token 使用和调用耗时等效率观测。指标存在不等于已经测得更便宜、更快，也不能直接跨不同模型价格比较。[评估入口](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/evaluation/agent_evaluator.py#L118)、[指标枚举](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/evaluation/eval_metrics.py#L58)

真实评估需要代表性数据、预期结果、阈值、模型配置及可能产生费用的调用；部分依赖由 eval extra 提供。本仓库的确定性 pytest 测试只检查示例控制流，不是 Agent 质量评测，没有在此伪造评分或延迟数据。[依赖范围](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/pyproject.toml#L197)

## 观测需要从事件走到上下文

Event 能回答“调用了哪个工具、产生了什么状态变化”；节点路径能区分同一工作流里的来源；trace 负责串起一次调用。BasePlugin 提供用户消息、run、agent、model、tool 和错误等生命周期钩子，可以接入观测或策略。但返回值可能改变执行路径，监控插件同样需要验证，不是完全被动的监听器。[插件接口](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/plugins/base_plugin.py#L41)

adk web 与开发 API 有助于查看会话、事件与调试信息。开发 UI 不等于公开生产网关；上线时需另行配置认证、授权、日志脱敏和数据保留。[CLI 源码](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/cli)
