import pytest


@pytest.mark.parametrize(
    "decision,actions,final",
    [
        ("approve", ["record_approval"], "已批准：记录本地动作"),
        ("reject", [], "已拒绝：未执行动作"),
    ],
)
async def test_resume_respects_human_decision(load_example, decision, actions, final):
    result = await load_example("04-human-in-the-loop").run_demo(decision)
    assert result.paused_before_action is True
    assert result.executed_actions == actions
    assert result.final_text == final


async def test_invalid_decision_is_rejected(load_example):
    with pytest.raises(ValueError, match="decision must be approve or reject"):
        await load_example("04-human-in-the-loop").run_demo("maybe")
