import pytest


async def test_real_runner_executes_the_requested_tool(load_example):
    result = await load_example("01-tool-agent").run_demo()
    assert result.tool_calls == [{"name": "get_weather", "args": {"city": "杭州"}}]
    assert result.final_text == "杭州：晴，24°C"
    assert any(event.get_function_responses() for event in result.events)


@pytest.mark.parametrize("missing", ["GOOGLE_API_KEY", "ADK_MODEL", "both"])
def test_live_mode_requires_both_settings(load_example, monkeypatch, capsys, missing):
    monkeypatch.setenv("GOOGLE_API_KEY", "not-a-real-key")
    monkeypatch.setenv("ADK_MODEL", "not-a-real-model")
    for name in ("GOOGLE_API_KEY", "ADK_MODEL"):
        if missing in (name, "both"):
            monkeypatch.delenv(name)
    assert load_example("01-tool-agent").main(["--live"]) == 2
    error = capsys.readouterr().err
    assert "GOOGLE_API_KEY" in error and "ADK_MODEL" in error
