# Google ADK 源码剖析与实践：设计方案

- 日期：2026-09-28
- 状态：用户已批准设计与计划；Native 实施完成，最终独立审阅完成且重要发现已处理，仅本地交付。
- 项目形态：独立的中文文档与示例仓库。
- 暂定仓库名：google-adk-explained。
- 分析对象：google/adk-python；其他语言实现只作为背景链接。
- 首版基线：v2.10.0，提交 53b3706e04fab34d1d53808a5f62cfe9b025f893。
- 交付限制：全部成果保留本地。不得创建远程仓库、推送分支、发起 PR、部署 Pages 或发布 Release，除非用户之后明确授权。
- 当前文档仅保存设计决策；下文的文件、测试与检查均为实施要求，不表示已经创建或通过。

## 1. 目标与已确认的需求

用户希望基于源码分析建立一个符合 GitHub 仓库惯例的 Google ADK 剖析项目。内容覆盖五个方面：项目概览、架构设计、核心功能、特色与竞品比较、使用与上手。README 必须展示架构图。

用户已确认：

1. 同时面向有 Python 基础、希望理解原理并落地 ADK 的开发者，以及需要评估 Agent 框架的技术负责人。
2. 采用“README 总览＋专题文档＋示例”的组织方式。
3. 接受五个主题、四个竞品、四个示例的首版范围。
4. 完成后先保留在本地，不提交到 GitHub。

项目应帮助读者回答：ADK 是否适合自己的场景、一次请求如何在框架内运行、如何用可复现的例子验证关键行为。分析以机制、证据和使用边界为主，不以官方 README 翻译或 API 罗列代替解释。

## 2. 范围与取舍

首版交付完整的五个主题、三张架构图、四个可运行 ADK 示例，以及仓库维护文件和本地质量检查。中文为主，保留 Python 标识符及必要英文术语，首次出现时解释其含义。

首版不建设独立网站，不生成全量 API 文档，不制作跨框架性能排行榜，不实现四个竞品的完整示例，也不修改 ADK 上游代码。实时音视频、云部署、MCP/A2A、评估等能力提供源码分析、使用条件与官方入口；四个核心示例负责验证最重要的运行机制。

这些是范围选择，不是对 ADK 或竞品能力的否定。以后新增专题需说明新增问题、证据和维护成本。

## 3. 两条阅读路径与 README

README 是进入项目的主要入口，按下列顺序组织：

1. 项目名称、独立社区分析身份、价值说明和分析版本。
2. 适合的读者，以及“技术选型”和“开发落地”两条阅读路径。
3. ADK 的定位、核心概念与适用边界摘要。
4. 一张总体架构图，附图例和进入源码的链接。
5. 主要能力、特色与设计取舍的摘要。
6. 精简竞品比较表，链接到详细证据。
7. 最短可执行的安装、离线验证和真实模型运行入口。
8. 五个主题的目录、贡献方式、帮助渠道和许可证。

选型路径为“概览 → 能力与限制 → 对比 → 最小验证”；开发路径为“上手 → 架构 → 专题 → 示例与测试”。

README 不承担所有源码细节。正文目标为约 1,500–2,500 个中文字，不包含代码和表格；这是编辑目标，不是机械字数门槛。徽章仅展示真实版本、许可证与已配置检查的状态；不制作虚构覆盖率或未运行的 CI 徽章。

## 4. 五个主题的内容设计

### 4.1 项目概览

docs/overview/index.md 解释框架定位、问题域、代码优先和组件组合等理念，明确 Agent 框架、模型 SDK、托管运行服务各自的边界。

docs/overview/selection-guide.md 用具体场景讨论采用 ADK 的理由、投入与限制，包括现有 Python 应用、复杂流程、跨模型需求、Google Cloud 集成需求。每个判断注明成立条件，避免把“支持某种集成”写成“必须依赖某家云”。

docs/overview/glossary.md 提供 Agent、Runner、Workflow、Node、Invocation、Context、Event、Session、State、Memory、Artifact 等术语的简短区分。

### 4.2 架构设计

docs/architecture/index.md 给出模块职责，并链接 README 中的总体图，避免重复维护图定义。

docs/architecture/request-lifecycle.md 沿一条真实异步调用链解释：入口、运行配置和调用上下文、节点执行、模型请求、工具执行、事件产出、会话保存与输出。单独标明 run_async 与 live 路径的差别，不把所有路径画成相同调用链。

docs/architecture/state-and-events.md 解释配置对象、一次调用的上下文、一次节点执行的上下文、会话状态和长期服务之间的生命周期；说明哪些对象共享、哪些结果会持久化，以及状态写入的边界。

docs/architecture/source-map.md 将关键概念映射到固定提交的文件、类、方法和相关测试，并说明公开 API 与内部实现的区别。

架构以实际源码为准。Runner、NodeRunner、Workflow、Agent 的箭头必须标明是调用、包含、继承还是数据流，不能混用。

### 4.3 核心功能

docs/capabilities/index.md 作为能力导航，正文拆成四篇：

- agents-and-workflows.md：Agent、函数节点、图编排、路由、并行、循环和结构化委派；区分现有工作流 Agent 与图运行时。
- tools-and-models.md：函数工具、模型适配、MCP、A2A、代码执行及认证边界；注明额外依赖。
- state-memory-and-hitl.md：Session、State、Memory、Artifact、人工介入与恢复，解释配置要求和失败情况。
- evaluation-observability-deployment.md：评估、追踪、开发 UI、实时交互和部署；区分 SDK 内部能力、独立组件与托管服务。

每篇使用统一写作骨架：要解决的问题 → 运行机制 → 源码证据 → 示例或测试 → 限制与适用场景。API 细节只保留帮助理解机制或做出选择的部分。

### 4.4 特色与竞品比较

docs/comparison/index.md 提供简表；docs/comparison/framework-tradeoffs.md 展开证据和场景化取舍。范围为 ADK、LangGraph、OpenAI Agents SDK、PydanticAI、CrewAI。

比较采用统一维度：

- 核心抽象与编排控制；
- 工具及模型接入；
- 状态、持久化、暂停与恢复；
- 类型约束与结构化输出；
- 人工介入；
- 调试、追踪与评估；
- 多模态和实时交互；
- 部署方式、生态依赖和应用侧需要承担的工作。

每项标明“框架内置”“通过扩展集成”“依赖托管服务”“由应用实现”及适用条件，不用简单勾叉隐藏差异。查不到足够证据时写明尚未核实，不把缺少文档等同于不支持。

标题采用“特色与设计取舍”。只有核查比较范围后，才将某项能力表述为该范围内的独有特性。不给未经实测的速度、成本或质量排名。

各竞品在实施研究开始时记录所分析的正式版本及提交；引用滚动更新的官方文档时记录核查日期和对应章节。若文档能力无法对应所分析版本，则将其单列为当前文档描述，不能混入版本比较结论。

### 4.5 使用与上手

docs/getting-started/index.md 提供最短安装与验证路径；environment.md 解释 Python、依赖、环境变量和模型配置；debugging.md 解释 CLI、开发 UI、事件观察和常见错误；production-checklist.md 提供从示例迁入实际应用时的状态后端、认证、评估、观测与部署决策。

默认开发与演示环境使用 Python 3.12，依赖固定 google-adk==2.10.0。示例的最低支持版本为 Python 3.10，并在该版本与 3.12 上执行离线检查；不据此声称覆盖 ADK 全部支持版本。

真实模型的型号放入环境变量，示例给出经官方文档核查的参考值。缺少凭证时应给出清楚的配置提示，不擅自调用云服务，也不将离线模拟输出当作真实模型响应。

## 5. 架构图设计

使用 GitHub 原生 Mermaid，并提供足够的文字说明，使无法显示图表的读者也能理解结论。

1. README 总体图：应用入口、Runner、节点执行、Agent/Workflow、模型与工具、事件和持久化服务。控制在约 12 个主要节点，细节链接到专题。
2. 请求时序图：以一个实际工具调用的异步请求为例，展示模型调用、工具结果返回、事件保存与最终输出的顺序。
3. 状态边界图：区分共享配置、InvocationContext、节点 Context、Session/State、Memory 和 Artifact 的生命周期及关系。

图的定义直接保存在引用它的 Markdown 中，避免多份源文件失去同步。README 总体图由架构专题引用，专题不再复制同一份定义。需验证 Mermaid 语法；若没有在 GitHub 上实际渲染，只能记录本地语法或渲染结果。

## 6. 四个示例与可验证的行为

所有示例均包含独立 README、运行入口、输入输出说明、相关专题与源码链接。共用项目根目录依赖配置和锁文件。

| 示例 | 演示内容 | 离线验收 |
| --- | --- | --- |
| 01-tool-agent | Agent 接收请求、调用一个确定性 Python 工具、返回结果 | 真实 Runner 和工具执行；只替换外部模型响应；验证参数、调用次数和最终事件 |
| 02-session-state | 同一会话跨轮读取状态，不同会话保持隔离 | 验证状态更新的保存与读取，并验证另一会话没有意外继承该会话的值 |
| 03-workflow-routing | 根据输入路由到不同函数节点，再形成输出 | 不需要模型；验证被选分支、未选分支和结果；包含无效输入的失败路径 |
| 04-human-in-the-loop | 请求人工输入、暂停、在同一会话继续执行 | 暂停前受控动作未发生；提供恢复输入后执行并得到结果；记录支持的恢复条件 |

离线测试必须经过 ADK 的真实运行与状态接口，不能把 Runner、事件流和会话服务全部 Mock 后只验证自建逻辑。确定性模型替身仅用于移除远程推理的不确定性。

第 4 个示例使用本地、无外部副作用的演示动作。首版只对实际测试覆盖的暂停/恢复范围做承诺，不自动扩展为进程崩溃恢复或任意副作用的 exactly-once 保证。

需要模型的示例提供可选真实模型模式。未取得真实运行证据时，文档明确写“离线验证通过；真实模型模式未执行”，不留空泛的“测试通过”。

## 7. 拟建仓库结构

~~~text
google-adk-explained/
  README.md
  LICENSE
  THIRD_PARTY_NOTICES.md
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  CHANGELOG.md
  pyproject.toml
  uv.lock
  .env.example
  .gitignore
  docs/
    overview/
    architecture/
    capabilities/
    comparison/
    getting-started/
    references.md
    validation.md
    superpowers/
      specs/
      plans/
  examples/
    01-tool-agent/
    02-session-state/
    03-workflow-routing/
    04-human-in-the-loop/
  tests/
  scripts/
  .github/
    ISSUE_TEMPLATE/
      content-error.yml
      content-suggestion.yml
      config.yml
    pull_request_template.md
    workflows/
      quality.yml
~~~

每个主题目录有 index.md。使用仓库内相对链接，示例与文章相互链接。scripts 只承载必要的文档、链接或示例检查，不建设通用文档生成框架。

设计和实施计划保留在新仓库的 docs/superpowers 下，供后续维护追溯。当前规格先保存在独立本地工作区，实施时迁入新仓库；不向 ADK 上游提交这些项目规划文档。

## 8. 证据、引用和更新规则

docs/references.md 保存证据索引，至少包含：结论主题、来源类别、官方 URL 或固定提交源码链接、版本/提交、核查日期、验证方式及限制。

源码结论使用提交 SHA 固定链接，链接到有关类或方法的准确行号。原理说明应至少有一个代码入口或测试证据；官方宣传性陈述不能独立支撑关于实际机制的结论。

明显区分三类内容：源码和测试确认的事实、官方文档描述、作者根据证据作出的分析。篇幅和表达允许不同，但读者必须能看出证据强弱。

基线不会自动跟随 main。更新版本需重跑示例、复核源码链接与关键结论，并在 CHANGELOG 中记录变化。这个规则是维护流程，不创建定时任务。

## 9. GitHub 仓库惯例与许可

README 解释用途、价值、上手方式、帮助渠道和维护方式。CONTRIBUTING 规定内容纠错、来源质量、示例验证、版本更新和 PR 审阅要求。Issue 模板分别收集“已有内容错误”和“新增主题建议”，不把上游 ADK 缺陷报告混入本仓库维护。

采用 Apache-2.0 作为项目原创文档、图和示例的许可证。引用或改编的上游片段保留其必要的版权与许可信息，列入 THIRD_PARTY_NOTICES；许可证不覆盖被引用项目的名称、商标或第三方材料。

项目声明为独立社区分析，链接官方项目；不使用会造成官方归属误解的命名、徽章或描述。行为准则说明尊重协作、报告和维护者处理原则；不虚构联系邮箱，涉及 GitHub 平台骚扰可指向平台的 Report abuse 渠道。

这些维护文件是本项目选用的开源协作惯例，不声称全部都是 GitHub 建仓的强制条件。

## 10. 质量检查与错误处理

quality.yml 在未来由用户发布后，才有机会在 GitHub 运行；当前只创建配置并执行能在本地运行的同等检查。检查内容为 Markdown 格式、相对链接与锚点、Mermaid 语法、Python 静态检查以及离线示例测试。

- 内部链接或锚点缺失：修复后再交付。
- 外部链接失败：区分真实失效、权限限制和瞬时网络错误；保存失败类别，不以全部忽略来获得全绿结果。
- 源码与文档冲突：以固定版本源码和可复现测试说明差异，避免静默拼接不同版本。
- 缺少 API Key：离线测试继续可用，真实模型运行提示配置要求。
- 示例异常：保留可理解的错误信息和非零退出状态，不静默吞掉异常。
- 无法完成某项验证：在 docs/validation.md 记录命令、环境、结果和未覆盖范围。

文档和示例使用的 Python 片段须做语法检查；标为“完整可运行”的片段还要验证导入和执行。仅供说明的节选必须标注上下文要求。

## 11. 验收标准

| 编号 | 完成条件 |
| --- | --- |
| A1 | 五个主题都有实质内容，并为两类读者提供清楚的阅读路径 |
| A2 | README 含可解析架构图、版本基线、比较摘要和可执行上手入口 |
| A3 | 三张图的职责、调用和状态关系与固定版本源码一致 |
| A4 | 核心架构及能力结论可追溯到官方资料、源码或测试 |
| A5 | 四个竞品采用统一维度，明确版本与能力实现条件 |
| A6 | 四个示例的离线行为验证在 Python 3.10 和 3.12 上有实际记录 |
| A7 | 真实模型、实时连接和云部署的未验证范围明确记录 |
| A8 | 文档内部链接、代码片段和示例检查完成；剩余限制如实说明 |
| A9 | 许可证、来源说明、贡献指南、行为准则和模板齐全 |
| A10 | 完整结果仅保留本地；没有远程建仓、推送或发布行为 |

## 12. 实施前后的交接

本设计经过自审后，先请用户审阅书面规格。用户批准后再使用 writing-plans 编写实施计划，明确任务顺序、具体文件、检查命令与执行方式；计划获得审阅且用户选择执行方式后，才开始创建项目内容。

实施时建立独立的本地仓库，不向当前 ADK 源码工作区添加分析文章或示例。可用的本地父目录和写权限在实施前检查；最终路径写入交付说明，不因目录不可写而自动改为远程发布。

完成交付包括本地仓库路径、README 和主要章节链接、验证结果与限制，以及当前版本的变更说明。用户之后如要求发布，再核实账号、仓库名与可见性；当前没有发布授权。

## 13. 已核查的初始资料

以下来源用于确定设计范围；它们不能替代实施阶段逐项核对具体结论。

- [ADK v2.10.0 发布页](https://github.com/google/adk-python/releases/tag/v2.10.0)
- [ADK 固定版本公共入口](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/__init__.py)
- [ADK 固定版本 BaseNode](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/workflow/_base_node.py)
- [LangGraph 概览](https://docs.langchain.com/oss/python/langgraph/overview)
- [OpenAI Agents SDK 官方概览](https://developers.openai.com/api/docs/guides/agents/sdk)
- [PydanticAI 概览](https://pydantic.dev/docs/ai/overview/)
- [CrewAI 概览](https://docs.crewai.com/v1.15.22/en/introduction)
- [GitHub README 指南](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [GitHub Mermaid 图表说明](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)
- [GitHub 健康贡献指南](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions)

## 14. 设计自审记录

- 范围：首版保持五个主题、四个竞品、四个 ADK 示例；网站和跨框架性能实验不在范围内。
- 一致性：README 是摘要入口，专题提供证据，示例与验证记录相互对应。
- 明确性：固定源码基线；竞品滚动文档需注明日期；离线与真实模型验证分别记录。
- 发布限制：用户最新的“完成后先别提交到 GitHub”指令贯穿交付和验收。
- 阶段边界：当前完成的是规格，不把计划中的文件和检查写成已完成成果。
