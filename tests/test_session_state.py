import pytest


async def test_shared_runner_preserves_session_boundaries(load_example):
    result = await load_example("02-session-state").run_demo()
    assert result.same_session_values == [1, 2]
    assert result.other_session_value == 1
    assert result.other_user_value == 1


@pytest.mark.parametrize("missing", ["GOOGLE_API_KEY", "ADK_MODEL", "both"])
def test_live_mode_requires_both_settings(load_example, monkeypatch, capsys, missing):
    monkeypatch.setenv("GOOGLE_API_KEY", "not-a-real-key")
    monkeypatch.setenv("ADK_MODEL", "not-a-real-model")
    for name in ("GOOGLE_API_KEY", "ADK_MODEL"):
        if missing in (name, "both"):
            monkeypatch.delenv(name)
    assert load_example("02-session-state").main(["--live"]) == 2
    assert "GOOGLE_API_KEY" in capsys.readouterr().err
