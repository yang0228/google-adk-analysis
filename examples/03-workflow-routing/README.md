# 03 · 确定性图路由

在仓库根运行：

```sh
uv run python examples/03-workflow-routing/main.py --text '你好？'
uv run python examples/03-workflow-routing/main.py --text '你好'
```

分别得到 question 与 statement，visited 列表只包含对应分支一次。完整可运行代码：[main.py](main.py)。

输入先去空白；中文或英文问号结尾选择 question，其余选择 statement；空输入报错。分类函数生成 Event(route=...)，实际 Workflow 调度对应分支，分支函数才追加 visited。最终文字来自该分支的输出事件。[测试](../../tests/test_workflow_routing.py)防止外层判断正确、图却执行两个分支的假通过。

这是一条可预测规则，不做自然语言意图理解。上游[路由示例](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/contributing/samples/workflows/route/agent.py#L25)使用 LLM 分类；这里替换为确定规则，便于离线观察图调度，没有模型费用。
