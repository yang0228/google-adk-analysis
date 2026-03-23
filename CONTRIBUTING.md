# 贡献指南

欢迎修正文档事实、改进解释或补充可复现示例。当前仓库仅在本地准备，GitHub 模板是未来发布时使用的配置。

## 内容标准

- 技术结论优先引用固定 commit 的源码与测试；官方滚动文档注明核查日期。
- 区分源码事实、官方描述、本地运行结果和分析判断。未实测的能力如实说明。
- 比较框架时使用同一维度，区分内置、扩展、托管、应用实现；不要用缺少证据证明“不支持”。
- 示例避免副作用，默认不需要模型凭证。涉及真实调用时说明配置与费用条件。
- 新增代码优先验证外部可见行为，不为纯文案修改添加无意义测试。

## 版本更新

先选定发布标签并解引用到 commit，更新依赖和锁文件，再检查受影响的源码链接、架构箭头、示例与比较结论。保留升级前后差异和验证限制；不要只改首页版本号。

## 本地检查

Python 3.12 和 Node.js 22 下，在仓库根执行：

```sh
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
```

只改文档可先跑对应检查；提交前运行相关检查并记录实际结果。图表还需目视检查文字、方向与含义。文档检查仅编译 Python 片段，不自动执行任意 Markdown 代码。

## 提出变更

说明读者遇到的问题、修改后行为、版本依据和验证。事实纠错附准确路径及源码链接；示例修改附输入、实际/预期结果。GitHub 发布后可使用仓库自身 Issue/PR 模板；上游 ADK 产品缺陷应先核对[官方 Issue](https://github.com/google/adk-python/issues)。

不要附 Key、私有会话或未经许可的数据。遵循[行为准则](CODE_OF_CONDUCT.md)；新增材料按[来源规则](THIRD_PARTY_NOTICES.md)署名。贡献以本仓库 [Apache-2.0](LICENSE) 许可提供，请确认你有权提交相应内容。
