import pytest


@pytest.mark.parametrize(
    "text,route",
    [
        ("你好？", "question"),
        ("hello?", "question"),
        ("  hello?  ", "question"),
        ("你好", "statement"),
    ],
)
async def test_only_selected_branch_executes(load_example, text, route):
    result = await load_example("03-workflow-routing").run_demo(text)
    assert result.route == route
    assert result.visited == [route]
    assert (
        result.final_text == ("收到问题：" if route == "question" else "收到陈述：") + text.strip()
    )


async def test_empty_input_is_rejected(load_example):
    with pytest.raises(ValueError, match="input must not be empty"):
        await load_example("03-workflow-routing").run_demo("   ")
