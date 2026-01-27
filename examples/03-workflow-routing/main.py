"""Route deterministic text through a real ADK Workflow."""

import argparse
import asyncio
import json
from dataclasses import asdict, dataclass

from google.adk import Event, Runner, Workflow
from google.adk.sessions import InMemorySessionService
from google.genai import types


@dataclass
class RoutingDemoResult:
    route: str
    visited: list[str]
    final_text: str


async def run_demo(text: str) -> RoutingDemoResult:
    text = text.strip()
    if not text:
        raise ValueError("input must not be empty")
    visited = []

    def classify(node_input: str):
        route = "question" if node_input.endswith(("?", "？")) else "statement"
        yield Event(output=node_input, route=route)

    def question(node_input: str):
        visited.append("question")
        return "收到问题：" + node_input

    def statement(node_input: str):
        visited.append("statement")
        return "收到陈述：" + node_input

    workflow = Workflow(
        name="router",
        edges=[("START", classify), (classify, {"question": question, "statement": statement})],
    )
    service = InMemorySessionService()
    await service.create_session(app_name="routing_demo", user_id="reader", session_id="demo")
    route = ""
    final_text = ""
    async with Runner(app_name="routing_demo", node=workflow, session_service=service) as runner:
        async for event in runner.run_async(
            user_id="reader",
            session_id="demo",
            new_message=types.Content(role="user", parts=[types.Part(text=text)]),
        ):
            if event.actions.route in ("question", "statement"):
                route = event.actions.route
            if isinstance(event.output, str):
                final_text = event.output
    return RoutingDemoResult(route, visited, final_text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", default="你好？")
    args = parser.parse_args(argv)
    try:
        result = asyncio.run(run_demo(args.text))
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(asdict(result), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
