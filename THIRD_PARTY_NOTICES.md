# 来源、署名与第三方许可

本仓库原创中文分析、Mermaid 与 SVG 图、验证脚本与示例以 [Apache-2.0](LICENSE) 提供。原创内容的版权归相应贡献者；Google、ADK 及各框架名称属于各自权利人，不表示授权、背书或隶属关系。

## Google ADK 参考材料

分析基线：google/adk-python v2.10.0，53b3706e04fab34d1d53808a5f62cfe9b025f893，上游采用 [Apache-2.0](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/LICENSE)。

示例 03 的图边/路由用法参考上游 [workflows/route](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/contributing/samples/workflows/route/agent.py)；示例 04 的 RequestInput 链与响应格式参考 [workflows/request_input](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/contributing/samples/workflows/request_input/agent.py)及[函数节点测试](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/tests/unittests/workflow/test_function_node.py)。相关上游文件声明 **Copyright 2026 Google LLC**。

这里保留来源署名。修改包括：去除真实模型与邮件场景，改为确定性文字路由、本地动作列表，添加 CLI、真实事件捕获和离线测试。没有把上游整段实现复制进本仓库，也没有对原创内容使用 Google 版权标头。

示例 01/02 是针对公开 API 编写的本地演示；工具天气数据是人工固定值。所有图均按源码重新绘制，没有复制官方品牌图。源码片段之外的事实与分析出处见[证据索引](docs/references.md)。

## 竞品与工具依赖

SVG 架构图的配色、圆角卡片与标题层级参考 [yang0228/deepseek-harness-analysis 的架构图](https://github.com/yang0228/deepseek-harness-analysis/tree/main/assets/diagrams)。节点、连线、布局与说明按本仓库 ADK 分析重新绘制；Mermaid 定义保留在文档的折叠区中。

竞品章节链接各项目固定版本的官方源码和文档，以原创文字归纳，没有引入其运行时代码。Python/Node 依赖由各自包管理器安装，许可随其发行包；本仓库不重新许可第三方包，不提交依赖目录或源码快照。uv.lock 和 package-lock.json 用于固定本次解析版本。

如后续引入实质性第三方代码、图片或长段文字，应在变更中列出文件、来源版本、修改和许可要求，并保留必要声明。
