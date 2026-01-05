# Google ADK Analysis Guide Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建一个仅保留本地、面向 Python 开发者和技术选型者的 Google ADK 中文源码剖析仓库，交付五个主题、三张架构图和四个可验证示例。

**Architecture:** README 提供两条阅读路径与内容摘要，专题文档解释机制并引用固定版本源码，四个独立示例验证工具、状态、路由和人工介入。示例共用依赖锁定和测试工具，不封装新的 Agent 框架。文档检查与源码证据索引支持后续维护。

**Tech Stack:** Python 3.10/3.12、google-adk==2.10.0、uv、pytest、pytest-asyncio、pytest-socket、ruff；Markdown、Mermaid；Node.js 22、markdown-it、github-slugger、markdownlint-cli2、Mermaid CLI。

**Spec:** [已批准的设计方案](../specs/2026-09-28-google-adk-analysis-design.md)

**Status:** 11 项任务及一次独立审阅完成，重要发现已处理；仅本地交付。

## Global Constraints

- 项目形态：独立的中文文档与示例仓库；采用“README 总览＋专题文档＋示例”。
- 首版基线：v2.10.0，提交 53b3706e04fab34d1d53808a5f62cfe9b025f893。
- 默认开发与演示环境使用 Python 3.12，依赖固定 google-adk==2.10.0。
- 示例的最低支持版本为 Python 3.10，并在该版本与 3.12 上执行离线检查。
- 范围为五个主题、三张架构图、四个 ADK 示例；竞品为 LangGraph、OpenAI Agents SDK、PydanticAI、CrewAI。
- 原创文档、图和示例采用 Apache-2.0；第三方片段保留必要署名和许可。
- 固定源码链接；滚动官方文档注明核查日期；事实、官方描述与分析判断明确区分。
- 离线测试使用真实 ADK Runner、工具和会话接口，只替换外部模型响应。
- 真实模型、实时连接和云部署没有实际运行证据时，明确记录未验证。
- 全部成果保留本地。不得创建远程仓库、推送分支、发起 PR、部署 Pages 或发布 Release，除非用户之后明确授权。

## Review Focus

1. 无 API Key 或模型配置时误触发网络：Task 2 验证离线模式不访问网络，真实模型模式在缺少配置时以退出码 2 结束；Task 3 沿用该约定。
2. 复用同一 Agent/Runner 后状态泄漏：Task 3 验证同会话连续更新、不同会话隔离，以及不同用户使用同名 session_id 时隔离。
3. 中文问号、首尾空白与空输入改变路由：Task 4 验证中文/英文问号、普通陈述及空白输入，未选分支不能执行。
4. 人工拒绝或无效决定仍触发动作：Task 5 验证暂停前零动作、批准后一次动作、拒绝后零动作、无效决定被拒绝。
5. 文档检查漏掉带空格的路径、重复中文标题或代码围栏中的伪链接：Task 11 的临时文档夹具验证这些情况，并检查损坏锚点及不可编译的 Python 片段。

---

## 执行环境与文件职责

目标目录为 /Users/jason/repo/google-adk-explained，创建独立 Git 仓库，初始分支为 codex/initial-analysis，不配置 remote。当前规划工作区只承载规格和计划，不能直接当作新项目交付。

若目标已存在，先读取其 Git 状态和内容：属于本项目则继续；非空且属于其他工作则保留原样，解决路径冲突后再执行。写权限通过平台正常授权处理，不通过嵌套到 ADK 源码目录来绕开。

下文所有相对路径均以新仓库为根。只有已批准设计与本计划需要从规划工作区复制。源码快照、环境、日志和渲染产物放在忽略目录 .validation/；不提交上游整库、密钥、虚拟环境或节点依赖。

| 任务 | 文件职责 |
| --- | --- |
| 1 | 仓库身份、版本基线、证据索引、项目概览与术语 |
| 2–5 | 每个示例一个 main.py 和 README；各自的行为测试 |
| 6 | 架构主线、两张专题图、源码地图 |
| 7 | 四篇核心能力分析与导航 |
| 8 | 统一维度的竞品比较与选型依据 |
| 9 | README 总体图、完整上手路径、实际验证记录 |
| 10 | 许可、贡献流程、社区文件与更新记录 |
| 11 | 文档与图表检查、CI 配置、本地完整验收 |

代码任务先写能揭示缺失行为的测试，再实现并运行；文档任务以逐条证据审阅和实际示例验证验收，不为可逆文案改动编造测试。

示例可直接运行 main.py，测试通过 load_example 夹具加载对应模块。四个示例不相互导入；不同示例的确定性模型分别演示各自的响应机制，不建立通用运行时抽象。

## Task 1: 建立版本基线与可读的项目概览

**Files:** Create README.md、.gitignore、docs/references.md、docs/overview/index.md、docs/overview/selection-guide.md、docs/overview/glossary.md；复制 docs/superpowers/specs/2026-09-28-google-adk-analysis-design.md 与本计划。

**Interfaces:**

- Consumes：已批准规格中的基线和两类读者。
- Produces：证据编号 E-ADK-001 起；每条记录主题、类型、URL、版本/提交、日期、验证方式和限制，后续文档引用这些记录。

- [x] **Step 1:** 检查目标目录；新建独立本地仓库，运行 git init -b codex/initial-analysis。复制两份规划文档，记录 Git 作者身份，不改成他人身份。
- [x] **Step 2:** .gitignore 忽略 .venv/、.venv-310/、node_modules/、.validation/、缓存、.env 及本地密钥文件，显式保留 .env.example。运行 git check-ignore 检验真实配置被忽略而模板可跟踪。
- [x] **Step 3:** 只读取得固定 SHA 的 ADK 源码和发布资料，记录版本一致性；当前 /Users/jason/repo/adk-python 的 main 只能用于导航，不能直接充当固定版本证据。
- [x] **Step 4:** 完成三篇概览与证据索引。先解释 Agent/Runner/Workflow/Context/Event 的关系，再区分 State、Session、Memory、Artifact；选型判断注明条件。
- [x] **Step 5:** 写可独立阅读的初版 README，仅链接已存在的概览与证据文件，不先制造空章节或失效导航。
- [x] **Step 6:** 人工抽查至少五条概览结论及其固定版本来源；执行 git diff --check；确认 git remote -v 无输出。
- [x] **Step 7:** 仅提交本任务文件，本地提交说明：docs: establish the ADK analysis baseline。

## Task 2: 实现工具调用示例与离线测试环境

**Files:** Create pyproject.toml、uv.lock、.env.example、tests/conftest.py、tests/test_tool_agent.py、examples/01-tool-agent/main.py、examples/01-tool-agent/README.md。

**Interfaces:**

- load_example(name: str) -> ModuleType：pytest 夹具返回加载函数，以仓库根定位 examples/{name}/main.py；加载前登记独立模块名，避免不同示例及 dataclass 相互污染。
- main.py 中的 async run_demo(*, model: str | BaseLlm | None = None) -> ToolDemoResult；None 使用本例确定性模型。
- ToolDemoResult 包含 final_text: str、tool_calls: list[dict[str, Any]]、events: list[Event]。
- main(argv: list[str] | None = None) -> int：默认离线；显式 --live 要求 GOOGLE_API_KEY 和 ADK_MODEL，缺少时返回 2。
- .env.example 只提供空凭证和配置说明；运行时从环境读取，文档不暗示自动加载 .env。

- [x] **Step 1:** 配置非发布包项目，requires-python 为 >=3.10，固定 google-adk==2.10.0；开发依赖包含 pytest、pytest-asyncio、pytest-socket、ruff。用 uv 生成并提交锁文件；pytest 配置 asyncio_mode="auto"；addopts 包含 --disable-socket --allow-unix-socket，禁止互联网访问并允许 asyncio 所需 Unix socket。
- [x] **Step 2:** 写 load_example 夹具和下列测试，再运行 uv run pytest tests/test_tool_agent.py -q，确认因示例接口尚不存在而失败。

~~~python
async def test_real_runner_executes_the_requested_tool(load_example):
    result = await load_example("01-tool-agent").run_demo()
    assert result.tool_calls == [{"name": "get_weather", "args": {"city": "杭州"}}]
    assert result.final_text == "杭州：晴，24°C"
    assert any(event.get_function_responses() for event in result.events)

def test_live_mode_without_credentials_returns_two(load_example, monkeypatch, capsys):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("ADK_MODEL", raising=False)
    assert load_example("01-tool-agent").main(["--live"]) == 2
    assert "GOOGLE_API_KEY" in capsys.readouterr().err
~~~

- [x] **Step 3:** 实现 get_weather(city: str) -> dict[str, Any]，返回本地固定演示数据；本例 BaseLlm 子类先产出 FunctionCall，再根据实际 FunctionResponse 生成最终文本。通过真实 Runner 消费全部事件并关闭资源。
- [x] **Step 4:** 实现 run_demo 与 CLI。离线模型只替代模型返回，不能直接调用工具代替 ADK 执行。--live 校验先于远程模型构造；不要打印凭证。
- [x] **Step 5:** 运行同一测试命令应全通过；运行 uv run python examples/01-tool-agent/main.py --offline，应输出“杭州：晴，24°C”。真实模型输出不要求逐字等同确定性输出。
- [x] **Step 6:** 写 README，明确天气数据和模型替身的演示性质、事件观察方式及真实模型配置。仅提交本任务文件：feat: demonstrate tool execution through the ADK runner。

## Task 3: 验证跨轮状态与会话隔离

**Files:** Create examples/02-session-state/main.py、examples/02-session-state/README.md、tests/test_session_state.py。

**Interfaces:**

- Consumes：Task 2 的 load_example 夹具与环境变量、CLI 退出码约定。
- async run_demo(*, model: str | BaseLlm | None = None) -> StateDemoResult。
- StateDemoResult 字段为 same_session_values: list[int]、other_session_value: int、other_user_value: int。
- main(argv: list[str] | None = None) -> int：默认离线，--live 按 Task 2 的配置规则执行。
- 工具 increment_counter(tool_context: ToolContext) -> int 更新未加前缀的 session 级 counter；模型替身只安排工具调用并读取返回值。

- [x] **Step 1:** 写测试并确认 uv run pytest tests/test_session_state.py -q 因缺少示例而失败。

~~~python
async def test_shared_runner_preserves_session_boundaries(load_example):
    result = await load_example("02-session-state").run_demo()
    assert result.same_session_values == [1, 2]
    assert result.other_session_value == 1
    assert result.other_user_value == 1
~~~

- [x] **Step 2:** 复用一个 Agent、一个 Runner 和真实 InMemorySessionService；同一用户/session 连续调用两次，另一个 session 调用一次，另一个用户的同名 session 再调用一次。每次从会话服务重新读取已保存状态，不能只读工具持有的临时字典。
- [x] **Step 3:** 实现独立模型替身与 CLI；为缺少真实模型配置补充与 Task 2 等价的退出码测试。
- [x] **Step 4:** 测试应全通过；运行 uv run python examples/02-session-state/main.py --offline，打印与断言一致的状态摘要。
- [x] **Step 5:** README 区分本例测试的 session 级隔离、用户级/应用级状态前缀及 InMemory 后端限制。提交：feat: verify session state across reused runners。

## Task 4: 实现确定性工作流路由

**Files:** Create examples/03-workflow-routing/main.py、examples/03-workflow-routing/README.md、tests/test_workflow_routing.py。

**Interfaces:**

- async run_demo(text: str) -> RoutingDemoResult；包含 route: str、visited: list[str]、final_text: str。
- main(argv: list[str] | None = None) -> int 接受 --text；默认“你好？”。
- 去除首尾空白后，以英文或中文问号结尾走 question，否则走 statement；空输入抛出 ValueError("input must not be empty")。

- [x] **Step 1:** 写参数化测试并先运行到失败。

~~~python
@pytest.mark.parametrize("text,route", [("你好？", "question"), ("hello?", "question"), ("  hello?  ", "question"), ("你好", "statement")])
async def test_only_selected_branch_executes(load_example, text, route):
    result = await load_example("03-workflow-routing").run_demo(text)
    assert result.route == route
    assert result.visited == [route]
    assert result.final_text

async def test_empty_input_is_rejected(load_example):
    with pytest.raises(ValueError, match="input must not be empty"):
        await load_example("03-workflow-routing").run_demo("   ")
~~~

- [x] **Step 2:** 使用公开 Workflow、Event(route=...)、函数节点和 Runner(node=...) 实现两个分支；visited 只由实际执行的分支函数写入。分支输出取自真实 Event，不以外层 if/else 直接完成整段流程。
- [x] **Step 3:** 运行 uv run pytest tests/test_workflow_routing.py -q，应全通过；运行 uv run python examples/03-workflow-routing/main.py --text '你好？'，应只出现 question 分支记录。
- [x] **Step 4:** README 解释规则路由与 LLM 分类路由的区别，并链接固定版本 route 示例。提交：feat: demonstrate deterministic workflow routing。

## Task 5: 实现人工介入的暂停与恢复

**Files:** Create examples/04-human-in-the-loop/main.py、examples/04-human-in-the-loop/README.md、tests/test_human_in_the_loop.py。

**Interfaces:**

- async run_demo(decision: str = "approve") -> ApprovalDemoResult。
- ApprovalDemoResult 包含 paused_before_action: bool、executed_actions: list[str]、final_text: str。
- main(argv: list[str] | None = None) -> int 接受 --decision approve|reject。
- 无效 decision 抛出 ValueError("decision must be approve or reject")，必须在运行任何演示动作之前拒绝。

- [x] **Step 1:** 核对固定版本 RequestInput、公开 Runner 恢复参数，以及对应测试中的 FunctionResponse 格式；将精确代码位置加入证据索引。恢复时使用实际捕获的 call ID 和 name，不猜测或硬编码随机 ID。RequestInput 使用 response_schema=str；恢复的 types.FunctionResponse.response 为 {"result": decision}，固定版本的 `_unwrap_response` 会取出 result 值，示例通过公开 types.Content/Part 和 Runner.run_async 发送响应，不导入内部工具函数。
- [x] **Step 2:** 写测试并确认 uv run pytest tests/test_human_in_the_loop.py -q 在实现前失败。

~~~python
@pytest.mark.parametrize("decision,actions", [("approve", ["record_approval"]), ("reject", [])])
async def test_resume_respects_human_decision(load_example, decision, actions):
    result = await load_example("04-human-in-the-loop").run_demo(decision)
    assert result.paused_before_action is True
    assert result.executed_actions == actions
    assert result.final_text

async def test_invalid_decision_is_rejected(load_example):
    with pytest.raises(ValueError, match="decision must be approve or reject"):
        await load_example("04-human-in-the-loop").run_demo("maybe")
~~~

- [x] **Step 3:** 构造由确定性函数节点组成的 Workflow，RequestInput 暂停后读取真实事件确认等待状态，并记录此时动作列表为空。再在相同会话用响应恢复：批准路径只向本地列表添加 record_approval，拒绝路径返回拒绝结果。
- [x] **Step 4:** 运行测试应全通过；分别执行 uv run python examples/04-human-in-the-loop/main.py --decision approve 和 --decision reject，核对动作分别为一次和零次。
- [x] **Step 5:** README 解释演示动作、响应标识和恢复范围；明确没有验证跨进程崩溃恢复或外部副作用 exactly-once。提交：feat: demonstrate approval and rejection across workflow resume。

## Task 6: 写架构专题、时序图和状态图

**Files:** Create docs/architecture/index.md、request-lifecycle.md、state-and-events.md、source-map.md；Modify docs/references.md、README.md。

**Interfaces:**

- Consumes：固定源码快照、四个示例与实际事件；不依赖竞品章节。
- Produces：请求时序 Mermaid 位于 request-lifecycle.md，状态边界 Mermaid 位于 state-and-events.md；总体图此时加到 README，Task 9 只整合布局而不复制图定义。

- [x] **Step 1:** 从公开 Runner.run_async 追踪实际执行路径，列出每个关键跳转的类/方法、固定 SHA 行号与相应测试；另行标记 live 路径差别。
- [x] **Step 2:** 写 source-map，覆盖 Agent、Runner、Workflow、BaseNode/NodeRunner、InvocationContext/Context、Event/EventActions、Session 服务、模型与工具处理器。
- [x] **Step 3:** 写两篇深入文章和架构导航；解释继承、调用、包含与事件流，不能将 Runtime 实现名称都标成稳定公共 API。
- [x] **Step 4:** 画三张 Mermaid 图，补充图例和文字替代说明；总览约 12 个主要节点，另外两图逐一对应源码与示例可见行为。
- [x] **Step 5:** 抽查一个带工具请求的完整顺序、一条状态保存路径、一个暂停/恢复边界；核对图中每个主要箭头。图语法和渲染由 Task 11 的统一工具完成。
- [x] **Step 6:** 提交：docs: explain ADK execution and state boundaries。

## Task 7: 写核心能力专题

**Files:** Create docs/capabilities/index.md、agents-and-workflows.md、tools-and-models.md、state-memory-and-hitl.md、evaluation-observability-deployment.md；Modify docs/references.md。

**Interfaces:** Consumes Task 6 的术语和调用链；Produces 规格 4.3 定义的能力导航和四篇文章，供 README、上手与比较章节链接。

- [x] **Step 1:** 对每个能力记录源码入口、依赖 extras、配置条件、演示/测试证据与限制；特别区分 MCP 工具协议和 A2A Agent 通信。
- [x] **Step 2:** 写 Agent/Workflow 与工具/模型两篇，沿实际对象和调用关系解释，不将“模型可替换”等同于所有模型支持全部高级能力。
- [x] **Step 3:** 写状态/HITL 与评估/观测/部署两篇；分别说明 Memory、Artifact、状态后端、实时连接、开发 UI 和托管组件的职责。
- [x] **Step 4:** 每篇按“问题→机制→证据→示例/测试→限制”审阅；检查标题中的所有能力是否有实质分析，未经运行的云和实时路径明确标注资料依据。
- [x] **Step 5:** 提交：docs: map ADK capabilities to mechanisms and limits。

## Task 8: 完成四个竞品的统一比较

**Files:** Create docs/comparison/index.md、framework-tradeoffs.md；Modify docs/overview/selection-guide.md、docs/references.md。

**Interfaces:** Consumes 固定 ADK 基线与规格规定的八个比较维度；Produces 至少五个框架在相同维度下的证据表，以及有条件的选型结论。

- [x] **Step 1:** 分别核查四个项目的官方版本、提交和文档；记录版本、日期。OpenAI 内容按 OpenAI Docs 官方来源顺序核查；不引用竞品营销文章来证明另一方缺失能力。
- [x] **Step 2:** 按核心编排、模型工具、状态恢复、类型输出、人工介入、观测评估、实时多模态、部署依赖逐项写证据。
- [x] **Step 3:** 给每格标明内置、扩展、托管或应用实现及必要条件；版本对应不清时单列文档描述，缺少证据写尚未核实。
- [x] **Step 4:** 写三个场景的取舍：现有 Python 应用中的结构化工具任务、需要人工审批的有状态流程、已有 Google Cloud 环境的 Agent 应用。引用事实后再给分析判断。
- [x] **Step 5:** 交叉检查“独有”“不支持”“更快”“更便宜”等措辞，删除无依据的绝对结论；提交：docs: compare agent frameworks with versioned evidence。

## Task 9: 完成上手路径与 README

**Files:** Create docs/getting-started/index.md、environment.md、debugging.md、production-checklist.md、docs/validation.md；Modify README.md、四个示例 README。

**Interfaces:** Consumes 已验证的示例命令与专题文件；Produces 规格第 3 节规定的完整首页和四篇上手文档。

- [x] **Step 1:** 写从 uv sync --locked 到四个离线命令的最短路径，解释 .env.example 的作用、如何显式设置环境变量及何时需要真实模型。
- [x] **Step 2:** 文档中的真实模型参考值通过对应提供商官方文档核查；未授权或未配置凭证时不执行在线调用，写明验证限制。
- [x] **Step 3:** 写调试与实际应用决策文档，沿 Event、模型请求、工具结果和 Session 定位问题；部署部分给出配置条件和官方入口，不声称完成云部署。
- [x] **Step 4:** 整合 README 的定位、读者路径、架构图、能力摘要、精简对比、快速开始和目录。仅把已有检查结果列为通过。
- [x] **Step 5:** 为所有 Python 围栏标明“完整可运行”或“片段”；完整示例优先链接仓库文件，需展示的完整代码必须与实测入口一致，避免维护第二份长脚本。
- [x] **Step 6:** 在清洁子进程中复制执行上手命令；记录操作系统、Python、ADK 版本、命令、退出码、输出摘要和未覆盖范围；提交：docs: provide reproducible reading and getting-started paths。

## Task 10: 补齐仓库协作与许可文件

**Files:** Create LICENSE、THIRD_PARTY_NOTICES.md、CONTRIBUTING.md、CODE_OF_CONDUCT.md、CHANGELOG.md、.github/ISSUE_TEMPLATE/content-error.yml、content-suggestion.yml、config.yml、.github/pull_request_template.md。

**Interfaces:** Consumes 已存在的内容与验证命令；Produces 面向未来贡献者的规则和模板，不执行任何 GitHub 写操作。

- [x] **Step 1:** 添加完整 Apache-2.0 许可证；逐项检查引入/改编的上游代码、图和文字，记录来源与许可，不将 Google 的版权主体用于项目原创内容。
- [x] **Step 2:** CONTRIBUTING 说明证据标准、固定版本更新、文档/示例检查和审阅流程；模板要求错误位置、版本、证据或建议收益。
- [x] **Step 3:** 行为准则说明尊重协作和处理原则，引用已有平台报告渠道，不编造邮箱或已开启的私密报告功能。
- [x] **Step 4:** CHANGELOG 记录本地首版，README 标明独立社区身份；模板的上游缺陷入口指向 ADK 官方仓库，仓库自身帮助链接使用相对文件或 GitHub 当前仓库上下文。
- [x] **Step 5:** 检查文档中的维护者身份、仓库 URL、状态徽章是否真实；本地未发布阶段不拼出不存在的仓库链接。提交：docs: define contribution and attribution practices。

## Task 11: 建立文档检查并完成本地验收

**Files:** Create package.json、package-lock.json、.markdownlint-cli2.jsonc、scripts/check_docs.mjs、scripts/check_diagrams.mjs、tests/test_check_docs.mjs、.github/workflows/quality.yml；Modify pyproject.toml、uv.lock（仅需补充开发工具时）、docs/validation.md、README.md。

**Interfaces:**

- check_docs.mjs 导出 async checkDocs(root: string, options: {pythonExecutable: string}) -> Promise<Problem[]>；Problem 字段 path: string、line: number、message: string。
- 命令 node scripts/check_docs.mjs --python .venv/bin/python：扫描根 README/维护文件、docs、examples；排除依赖和 .validation。用 markdown-it 解析代码围栏与链接、github-slugger 计算标题锚点；Python 片段只编译，不自动执行任意 Markdown 代码。
- check_diagrams.mjs 命令：提取上述文档中的 Mermaid，调用本地 mmdc，在 .validation/diagrams 下渲染；不改写源 Markdown。
- package.json 脚本为 lint:md、check:diagrams、test:docs。项目只使用 Node 开发工具，不建设前端。

- [x] **Step 1:** Node.js 22 下添加并精确锁定 markdown-it、github-slugger、markdownlint-cli2、@mermaid-js/mermaid-cli；提交 lockfile。编写文档检查的临时目录夹具，确认在实现检查器前失败。

~~~javascript
test("encoded paths and repeated Chinese headings resolve", async () => {
  assert.deepEqual(await checkDocs(validChineseAndEncodedPathFixture, opts), []);
});
test("a missing anchor is reported", async () => {
  assert.equal((await checkDocs(missingAnchorFixture, opts)).length, 1);
});
test("links inside fences are ignored", async () => {
  assert.deepEqual(await checkDocs(fakeLinkInsideFenceFixture, opts), []);
});
test("invalid Python is reported", async () => {
  assert.equal((await checkDocs(invalidPythonFenceFixture, opts)).length, 1);
});
~~~

夹具由测试在独立临时目录建立；opts.pythonExecutable 指向项目 .venv/bin/python。validChineseAndEncodedPathFixture 的 README 链接 docs/a%20b.md#概览-1，目标文件包含两个“# 概览”标题；missingAnchorFixture 仅将片段改为 #不存在；fakeLinkInsideFenceFixture 仅在 text 围栏中放置指向 missing.md 的链接；invalidPythonFenceFixture 包含 python 围栏“def broken(”。其余文件均保持合法，确保每次只验证一个错误条件。

- [x] **Step 2:** 实现链接和片段检查。带空格的目标经过 URL 解码，重复中文标题使用 GitHub slug 去重规则；代码围栏内伪链接不计入。错误必须给出文件和行号，不能总是返回空列表。
- [x] **Step 3:** 运行 node --test tests/test_check_docs.mjs，应全通过；运行 node scripts/check_docs.mjs --python .venv/bin/python，无问题时退出 0。
- [x] **Step 4:** 配置 Markdown lint；实现 Mermaid 渲染命令并运行三张实际图。手动查看 SVG，检查文字完整、节点不遮挡和箭头语义。浏览器不可用时记录限制，不冒充完成渲染。
- [x] **Step 5:** quality.yml 配置 Ubuntu、Python 3.10/3.12 离线示例矩阵与 Node.js 22 文档检查；最小权限 contents: read，不需要 API secrets。工作流只保存配置，不触发远程运行。
- [x] **Step 6:** 在项目根执行下列最终检查；若失败，只修复相关问题并重跑受影响项，最后记录完整结果。

~~~sh
uv sync --locked --python 3.12
uv run ruff check examples tests
uv run pytest -q
UV_PROJECT_ENVIRONMENT=.venv-310 uv sync --locked --python 3.10
UV_PROJECT_ENVIRONMENT=.venv-310 uv run pytest -q
npm ci
npm run lint:md
npm run test:docs
node scripts/check_docs.mjs --python .venv/bin/python
npm run check:diagrams
git diff --check
git remote -v
~~~

预期：静态检查无错误；两种 Python 的离线测试通过；文档、链接、片段与三图检查通过；没有 remote。实际数量和结果写入 validation，不预填。

- [x] **Step 7:** 执行四个示例 README 的全部离线命令；逐条对照 A1–A10。外部链接仅作只读核查，区分失效、受限与瞬时网络失败；补齐证据索引与验证限制。
- [x] **Step 8:** 按用户选择的执行方式做最终审阅并处理发现；提交：chore: validate the local ADK analysis guide。检查最终 Git 状态和文件清单，确保只交付本地成果。

## 覆盖与自审记录

| 规格验收 | 对应任务 |
| --- | --- |
| A1 五个主题及两条阅读路径 | 1、6、7、8、9 |
| A2 README 架构图、基线、对比与上手 | 1、6、8、9 |
| A3 三图与固定源码一致 | 6、11 |
| A4 核心结论可追溯 | 1、6、7、8 |
| A5 四竞品统一维度及版本 | 8 |
| A6 四示例双 Python 离线验证 | 2、3、4、5、11 |
| A7 在线/实时/部署限制 | 7、9、11 |
| A8 文档、链接、片段、示例检查 | 9、11 |
| A9 协作与许可文件 | 10 |
| A10 仅本地交付 | 全局限制、1、10、11 |

自审结论：规格五个主题和十项验收均有任务覆盖；示例接口及返回字段在所属任务定义，后续只消费已定义接口；五项 Review Focus 均落实到具体断言。文档任务采用来源与行为审阅，不人为套用代码 TDD。实施状态以复选框为准；实际验证结果与限制见 [validation](../../validation.md)。

## 执行方式与交付

推荐 Native：由当前助手连续实现，保持源码分析、比较用语和示例解释一致，最后安排一次独立审阅。另一个选项是 Subagent-driven：逐任务实现和独立审阅，复核更细，但会增加上下文切换与成本。已选择 Native 执行。

用户已批准计划并选择 Native，由当前助手实施并安排一次最终独立审阅。交付时提供本地仓库路径、README、主要专题、验证记录及剩余限制；不创建远程仓库、不推送、不部署。
