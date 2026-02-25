# 工具、模型与协议

## 工具执行有两个边界

工具声明把名称、参数与说明交给模型；实际执行由框架接收 FunctionCall、校验参数并调用 Python。FunctionTool.run_async 先做参数预处理，验证错误可作为结果返回模型；需要确认时先触发确认，拒绝后不调用函数。业务异常不应一概理解成会自动重试。[FunctionTool](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/tools/function_tool.py#L357)

[工具示例](../../examples/01-tool-agent/README.md)只替换 BaseLlm 的响应，保留真实参数、工具和 FunctionResponse。它验证接线正确，不能验证模型理解用户意图。真实服务工具仍要处理权限、限流、超时、输入大小和外部副作用。

## 可替换模型，不代表能力完全等价

BaseLlm.generate_content_async 是模型扩展入口；模型 capabilities 还表达具体能力，例如输出 schema 与工具能否同时使用。上下文窗口、多模态格式、实时连接和工具协议可能因模型及提供商而异。[BaseLlm](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/models/base_llm.py#L36)

v2.10.0 核心依赖包含 google-genai；OpenAI 适配器位于 google.adk.integrations.openai，使用 openai extra。LiteLLM 和 Anthropic 等集成涉及 extensions 中的依赖。不要只换模型字符串，就假定结构化输出、实时和推理参数保持同样语义。[依赖声明](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/pyproject.toml#L32)

## MCP 和 A2A 的区别

| 机制 | 接入对象 | 条件 | 应用仍承担 |
| --- | --- | --- | --- |
| Python 工具 | 本地函数 | 核心依赖，正确签名和说明 | 权限、超时、副作用 |
| McpToolset | 远程或子进程工具及资源 | mcp extra、连接参数、服务器与授权 | 服务器信任、凭证范围、断线处理 |
| RemoteA2aAgent | 远程 Agent | a2a extra、Agent 服务端点与认证 | 委托边界、会话映射、结果契约 |

MCP 解决工具与资源接入；A2A 解决 Agent 间通信。把 MCP server 当子 Agent 使用会遗漏任务生命周期，把 A2A 当普通本地函数会遗漏网络与权限边界。[McpToolset](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/tools/mcp_tool/mcp_toolset.py#L116)、[RemoteA2aAgent](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/a2a/agent/_remote_a2a_agent.py#L625)

## 代码执行器：执行什么、在哪里执行

当任务需要临时计算或处理数据时，LlmAgent.code_executor 可接收 BaseCodeExecutor。框架从模型响应提取代码、交给执行器，再把执行结果接回模型上下文；普通 FunctionTool 则调用应用事先定义好的函数。[配置入口](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/agents/llm_agent.py#L484)、[执行器契约](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/code_executors/base_code_executor.py#L30)、[响应处理](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/flows/llm_flows/extensions/_code_execution.py#L199)

| 执行方式 | 位置与机制 | 条件及边界 |
| --- | --- | --- |
| BuiltInCodeExecutor | 请求中启用模型提供商的代码执行工具 | 此版本针对 Gemini；可用模型与限制由提供商决定，需要在线调用 |
| UnsafeLocalCodeExecutor | 本机 Python 子进程执行生成代码，收集标准输出、错误及退出码 | 继承本机环境，子进程与超时控制不构成安全沙箱；不支持 stateful=True |
| ContainerCodeExecutor | 在 Docker 容器中执行代码 | 需要 Docker 服务与镜像，docker 依赖列于 extensions；默认禁用网络、移除 Linux capabilities，但应用仍需管理镜像、资源及运行边界 |

表中机制分别来自 [BuiltIn](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/code_executors/built_in_code_executor.py#L31)、[UnsafeLocal](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/code_executors/unsafe_local_code_executor.py#L120)、[Container](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/code_executors/container_code_executor.py#L130)及[扩展依赖](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/pyproject.toml#L210)。需要云端环境时还可检查仓库中的 Vertex AI、GKE 与 Agent Engine 执行器；具体云 SDK、账号和隔离条件要按所选实现配置，不能从“支持代码执行”推导为默认已具备这些环境。

上游[本地执行器测试](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/tests/unittests/code_executors/test_unsafe_local_code_executor.py#L114)展示输出、异常和超时等行为。本仓库只阅读这些实现和测试，没有执行生成代码、启动 Docker 或调用托管执行器；四个入门示例中的 Python 工具也不能作为这些执行环境的验证证据。

## 工具凭证怎样请求、返回和保存

调用外部 API 的工具可能需要用户凭证。AuthConfig 描述认证方案与凭证；工具通过上下文 request_credential 把请求写进 EventActions.requested_auth_configs，按当前 function_call_id 关联。框架把它转换成 adk_request_credential 事件，客户端完成认证后以匹配 ID 的 FunctionResponse 返回。认证预处理器结合此前的请求解析响应，保存凭证并确定要恢复的原工具调用。[请求入口](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/agents/context.py#L669)、[认证事件](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/flows/llm_flows/tools/_functions.py#L174)、[响应与恢复](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/auth/auth_preprocessor.py#L87)

AuthHandler 可执行必要的 token 交换，将响应写到 temp: 前缀状态；客户端可见的请求和会话中的凭证会移除 OAuth client secret，交换时从服务端工具配置补回。这个处理不等于移除用户 access/refresh token，更不等于已经实现应用业务权限。[AuthHandler](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/auth/auth_handler.py#L89)

凭证的持续保存由所配置的 CredentialService 决定。上下文 save_credential/load_credential 在没有服务时会报错；CredentialManager 的自动保存也以服务存在为前提。InMemoryCredentialService 按 app/user 分桶且仅存内存；SessionStateCredentialService 存入会话状态，其用户 token 可以被有权读取该状态的客户端看到，不能当成加密凭证库。[服务接口](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/agents/context.py#L622)、[保存条件](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/auth/credential_manager.py#L404)、[内存实现](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/auth/credential_service/in_memory_credential_service.py#L31)、[会话实现](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/auth/credential_service/session_state_credential_service.py#L34)

authlib 属于此版本核心依赖，但 OAuth 客户端、回调接收、授权范围和凭证后端仍需配置。模型 API Key、工具访问令牌与应用用户授权是不同边界。本仓库核对了[上游凭证响应测试](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/tests/unittests/auth/test_auth_handler.py#L779)，未运行 OAuth 往返或外部工具认证；[审批示例](../../examples/04-human-in-the-loop/README.md)演示业务决定，不能代替认证流验证。

## 真实配置的限制

本仓库没有连接 MCP/A2A 服务，也未调用任何真实提供商。扩展依赖的准确名称以[固定 pyproject](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/pyproject.toml#L58)为准；项目默认锁文件不包含这些可选集成。在线示例的配置检查只证明缺失 Key 或模型名时会及早退出，不证明该账号有模型访问权。
