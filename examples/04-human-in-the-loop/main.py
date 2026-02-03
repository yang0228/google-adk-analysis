"""Pause a Workflow and resume it with a local approval or rejection."""

import argparse
import asyncio
import json
from dataclasses import asdict, dataclass

from google.adk import Event, Runner, Workflow
from google.adk.events import RequestInput
from google.adk.sessions import InMemorySessionService
from google.genai import types


@dataclass
class ApprovalDemoResult:
    paused_before_action: bool
    executed_actions: list[str]
    final_text: str


async def run_demo(decision: str = "approve") -> ApprovalDemoResult:
    if decision not in ("approve", "reject"):
        raise ValueError("decision must be approve or reject")
    actions = []

    def request_approval():
        yield RequestInput(message="Approve the local demo action?", response_schema=str)

    def route_decision(node_input: str):
        if node_input not in ("approve", "reject"):
            raise ValueError("decision must be approve or reject")
        yield Event(route=node_input)

    def approved():
        actions.append("record_approval")
        return "已批准：记录本地动作"

    def rejected():
        return "已拒绝：未执行动作"

    workflow = Workflow(
        name="approval",
        edges=[
            ("START", request_approval, route_decision),
            (route_decision, {"approve": approved, "reject": rejected}),
        ],
    )
    service = InMemorySessionService()
    await service.create_session(app_name="approval_demo", user_id="reader", session_id="demo")
    async with Runner(app_name="approval_demo", node=workflow, session_service=service) as runner:
        paused_events = [
            event
            async for event in runner.run_async(
                user_id="reader",
                session_id="demo",
                new_message=types.Content(role="user", parts=[types.Part(text="Start review.")]),
            )
        ]
        requests = [
            (event, call)
            for event in paused_events
            for call in event.get_function_calls()
            if call.id in (event.long_running_tool_ids or set())
        ]
        if len(requests) != 1:
            raise RuntimeError("Expected exactly one pending input request")
        pause_event, call = requests[0]
        paused_before_action = not actions
        response = types.FunctionResponse(name=call.name, id=call.id, response={"result": decision})
        final_text = ""
        async for event in runner.run_async(
            user_id="reader",
            session_id="demo",
            invocation_id=pause_event.invocation_id,
            new_message=types.Content(role="user", parts=[types.Part(function_response=response)]),
        ):
            if isinstance(event.output, str):
                final_text = event.output
    return ApprovalDemoResult(paused_before_action, actions, final_text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decision", choices=("approve", "reject"), default="approve")
    args = parser.parse_args(argv)
    print(json.dumps(asdict(asyncio.run(run_demo(args.decision))), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
