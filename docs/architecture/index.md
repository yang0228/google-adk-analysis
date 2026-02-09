# 架构导航

先看 [README 总体图](../../README.md#架构总览)，再沿[一次请求](request-lifecycle.md)走进运行时，最后用[状态与事件](state-and-events.md)理解恢复边界。[源码地图](source-map.md)提供固定 SHA 的入口。

## 三层职责

声明层定义 Agent、工具、Workflow 的节点与边。运行层由 Runner 建立调用，并通过节点执行器驱动各节点；Workflow 在这一层进一步调度自己的图。服务层提供 Session、Memory、Artifact 等数据接口。模型提供商和远程工具是外部依赖，不是图调度器的一部分。

继承关系是 LlmAgent → BaseAgent → BaseNode，以及 Workflow → BaseNode；调用关系是 Runner 进入节点运行时，节点运行时调用节点实现。Workflow **不是 Runner 的父类**，Agent **不是 Session 的子类**。图中的包含关系也不等于 Python 继承。

## 一个需要保留的版本细节

v2.10.0 的 run_async 对根 LlmAgent 和非 BaseAgent 的 BaseNode 走节点运行时；剩余 BaseAgent 分支仍保留传统执行路径。不能据此说所有 Agent 都已统一迁移。LlmAgent 默认根模式是 chat，task 模式另有完成任务输出约定。对应源码见 [runners.py:1082](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/runners.py#L1082)。

下划线实现文件和 NodeRunner 用来解释执行机制。应用示例通过公开 Agent、Workflow、Runner、Event、RequestInput 等接口运行，不直接构造内部调度器。扩展前应阅读相关版本的 API 约定及测试，避免把源码中能导入的名称当成稳定接口。

## 先运行，再阅读

工具示例观察调用闭环；状态示例观察写回；路由示例观察只执行选定分支；审批示例观察暂停后的公开恢复参数。它们分别对应下文的模型、存储、调度与恢复四条主线。[四个示例入口](../../examples/01-tool-agent/README.md)
