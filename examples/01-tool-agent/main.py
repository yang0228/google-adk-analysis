"""Run a real ADK tool cycle; only the model response is deterministic offline."""

import argparse
import asyncio
import os
import sys
from dataclasses import dataclass
from typing import Any

from google.adk import Agent, Runner
from google.adk.events import Event
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.adk.sessions import InMemorySessionService
from google.genai import types


def get_weather(city: str) -> dict[str, Any]:
    """Return fixed demonstration weather, not a live weather service."""
    return {"city": city, "weather": "晴，24°C"}


class OfflineWeatherModel(BaseLlm):
    model: str = "offline-weather"

    async def generate_content_async(self, llm_request, stream=False):
        last = llm_request.contents[-1]
        responses = [p.function_response for p in last.parts or [] if p.function_response]
        if responses:
            result = responses[-1].response
            part = types.Part(text=f"{result['city']}：{result['weather']}")
        else:
            part = types.Part(
                function_call=types.FunctionCall(name="get_weather", args={"city": "杭州"})
            )
        yield LlmResponse(content=types.Content(role="model", parts=[part]))


@dataclass
class ToolDemoResult:
    final_text: str
    tool_calls: list[dict[str, Any]]
    events: list[Event]


async def run_demo(*, model: str | BaseLlm | None = None) -> ToolDemoResult:
    service = InMemorySessionService()
    agent = Agent(
        name="weather_agent",
        model=model or OfflineWeatherModel(),
        instruction="Call get_weather once for 杭州, then summarize its result.",
        tools=[get_weather],
    )
    await service.create_session(app_name="tool_demo", user_id="reader", session_id="demo")
    events = []
    async with Runner(app_name="tool_demo", agent=agent, session_service=service) as runner:
        async for event in runner.run_async(
            user_id="reader",
            session_id="demo",
            new_message=types.Content(role="user", parts=[types.Part(text="杭州天气如何？")]),
        ):
            events.append(event)
    calls = [
        {"name": call.name, "args": call.args}
        for event in events
        for call in event.get_function_calls()
    ]
    final = [
        part.text
        for event in events
        if event.is_final_response() and event.content
        for part in event.content.parts or []
        if part.text and not part.thought
    ]
    return ToolDemoResult("".join(final), calls, events)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--offline", action="store_true", help="Default; no network model calls")
    mode.add_argument("--live", action="store_true", help="Use a configured Gemini model")
    args = parser.parse_args(argv)
    model = None
    if args.live:
        if not all(os.environ.get(key, "").strip() for key in ("GOOGLE_API_KEY", "ADK_MODEL")):
            print("--live requires GOOGLE_API_KEY and ADK_MODEL.", file=sys.stderr)
            return 2
        model = os.environ["ADK_MODEL"]
    print(asyncio.run(run_demo(model=model)).final_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
