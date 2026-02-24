# Agent 与 Workflow：谁决定下一步

## 从任务性质选择执行方式

当下一步取决于自然语言语义，LlmAgent 可以基于指令和可用工具选择动作。当步骤顺序和条件可以明确写成程序，Workflow 的节点与边能固定这个结构。一个 Workflow 内既可以调用函数，也可以运行 Agent；两者不需要分成互不相干的应用。[继承与调度](../architecture/index.md)

SequentialAgent、ParallelAgent、LoopAgent 直接表达常见组合；Workflow 更显式地表示边、路由和节点输出。图调度器维护 ready nodes 和运行状态；max_concurrency 约束由图边触发的节点，源码明确排除动态 ctx.run_node 的内联调用。因此不能把它理解为整个系统所有任务的并发总上限。[Workflow 定义](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/workflow/_workflow.py#L131)

## Agent 不是只有“提示词加模型”

LlmAgent 包含工具、子 Agent、输入/输出约束和模式等配置。根 LlmAgent 默认 chat 模式，task 模式使用任务完成约定；这些选择影响结果怎样进入 Event.output。对子 Agent 的委托还涉及上下文范围，不能假设它无条件看见父节点的一切历史。[模式选择](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/runners.py#L1082)、[任务包装](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/workflow/_llm_agent_wrapper.py#L391)

条件路由可以来自规则，也可以来自模型结构化输出。前者用确定测试覆盖边界；后者还需要评估分类质量和错误分布。把模型输出声明成枚举能限制合法值，却不证明模型选对了类别。

## 用最小图观察真实行为

[路由示例](../../examples/03-workflow-routing/README.md)将英文/中文问号分到 question，普通文字分到 statement。分类节点只给 Event(route=...)，后续分支由 Workflow 调度。visited 在分支函数内部记录，证明未选分支没有执行。示例不需要扩展依赖或模型 Key。

这里“收到问题”是固定输出，完全不代表能回答问题。实际应用换成 LLM 后，原有路由测试仍有价值，但要另加模型评估。并行图中的冲突写、取消、失败补偿和循环终止条件也需要应用级测试。本例未覆盖这些场景。
