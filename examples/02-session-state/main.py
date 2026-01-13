"""Observe persisted state while reusing one Agent and Runner."""

import argparse
import asyncio
import json
import os
import sys
from dataclasses import asdict, dataclass

from google.adk import Agent, Runner
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.adk.sessions import InMemorySessionService
from google.adk.tools import ToolContext
from google.genai import types


def increment_counter(tool_context: ToolContext) -> int:
    """Increment this session's counter once."""
    value = tool_context.state.get("counter", 0) + 1
    tool_context.state["counter"] = value
    return value


class OfflineCounterModel(BaseLlm):
    model: str = "offline-counter"

    async def generate_content_async(self, llm_request, stream=False):
        last = llm_request.contents[-1]
        responses = [p.function_response for p in last.parts or [] if p.function_response]
        if responses:
            part = types.Part(text=f"counter={responses[-1].response['result']}")
        else:
            part = types.Part(function_call=types.FunctionCall(name="increment_counter", args={}))
        yield LlmResponse(content=types.Content(role="model", parts=[part]))


@dataclass
class StateDemoResult:
    same_session_values: list[int]
    other_session_value: int
    other_user_value: int


async def run_demo(*, model: str | BaseLlm | None = None) -> StateDemoResult:
    service = InMemorySessionService()
    agent = Agent(
        name="counter_agent",
        model=model or OfflineCounterModel(),
        instruction="Call increment_counter exactly once per user message, then report it.",
        tools=[increment_counter],
    )
    for user_id, session_id in (("alice", "one"), ("alice", "two"), ("bob", "one")):
        await service.create_session(app_name="state_demo", user_id=user_id, session_id=session_id)
    values = []
    async with Runner(app_name="state_demo", agent=agent, session_service=service) as runner:
        for user_id, session_id in (
            ("alice", "one"),
            ("alice", "one"),
            ("alice", "two"),
            ("bob", "one"),
        ):
            async for _event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=types.Content(role="user", parts=[types.Part(text="Increment once.")]),
            ):
                pass
            saved = await service.get_session(
                app_name="state_demo", user_id=user_id, session_id=session_id
            )
            values.append(saved.state["counter"])
    return StateDemoResult(values[:2], values[2], values[3])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--offline", action="store_true")
    mode.add_argument("--live", action="store_true")
    args = parser.parse_args(argv)
    model = None
    if args.live:
        if not all(os.environ.get(key, "").strip() for key in ("GOOGLE_API_KEY", "ADK_MODEL")):
            print("--live requires GOOGLE_API_KEY and ADK_MODEL.", file=sys.stderr)
            return 2
        model = os.environ["ADK_MODEL"]
    print(json.dumps(asdict(asyncio.run(run_demo(model=model))), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
