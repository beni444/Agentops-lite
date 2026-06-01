import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools import TOOLS
from prompts import SYSTEM_PROMPT
from trace import TraceLogger
from config import MODEL_NAME

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

CONFIRMATION_WORDS = ["yes", "confirm", "go ahead", "please issue", "approve", "do it"]
STATE_CHANGING_TOOLS = {"issue_refund"}

def is_confirmed(user_input):
    return any(word in user_input.lower() for word in CONFIRMATION_WORDS)

def build_tool_declarations():
    return [
        types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="get_order_status",
                    description="Get the current status of a customer order.",
                    parameters={
                        "type": "object",
                        "properties": {
                            "order_id": {
                                "type": "string",
                                "description": "The customer order ID."
                            }
                        },
                        "required": ["order_id"],
                    },
                ),
                types.FunctionDeclaration(
                    name="check_refund_eligibility",
                    description="Check whether an order is eligible for a refund before processing it.",
                    parameters={
                        "type": "object",
                        "properties": {
                            "order_id": {
                                "type": "string",
                                "description": "The customer order ID."
                            }
                        },
                        "required": ["order_id"],
                    },
                ),
                types.FunctionDeclaration(
                    name="check_return_eligibility",
                    description="Check whether an order is eligible for return.",
                    parameters={
                        "type": "object",
                        "properties": {
                            "order_id": {
                                "type": "string",
                                "description": "The customer order ID."
                            }
                        },
                        "required": ["order_id"],
                    },
                ),
                types.FunctionDeclaration(
                    name="issue_refund",
                    description="Issue a refund for an eligible order.",
                    parameters={
                        "type": "object",
                        "properties": {
                            "order_id": {
                                "type": "string",
                                "description": "The customer order ID."
                            }
                        },
                        "required": ["order_id"],
                    },
                ),
                types.FunctionDeclaration(
                    name="create_ticket",
                    description="Create a customer support ticket.",
                    parameters={
                        "type": "object",
                        "properties": {
                            "issue": {
                                "type": "string",
                                "description": "The customer issue to log."
                            }
                        },
                        "required": ["issue"],
                    },
                ),
            ]
        )
    ]


def extract_function_call(response):
    try:
        candidate = response.candidates[0]
        for part in candidate.content.parts:
            if getattr(part, "function_call", None):
                return part.function_call
    except Exception:
        return None

    return None


def run_agent(user_input, conversation_history):
    trace_logger = TraceLogger()

    print("\n🧠 AGENT START")
    print("User:", user_input)

    conversation_history.append(
        types.Content(
            role="user",
            parts=[types.Part(text=user_input)]
        )
    )

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=build_tool_declarations(),
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=conversation_history,
        config=config,
    )

    function_call = extract_function_call(response)

    while function_call:
        tool_name = function_call.name
        tool_args = dict(function_call.args)

        print(f"\n🔧 Tool: {tool_name} | Args: {tool_args}")

        if tool_name not in TOOLS:
            tool_result = {"error": f"Unknown tool: {tool_name}"}

        elif tool_name in STATE_CHANGING_TOOLS and not is_confirmed(user_input):
            final_output = (
                f"I can help with that, but I need your confirmation before processing a refund "
                f"for order {tool_args.get('order_id')}. Please confirm if you'd like me to proceed for a refund."
            )

            print("\n🧾 FINAL OUTPUT:")
            print(final_output)

            conversation_history.append(
                types.Content(
                    role="model",
                    parts=[types.Part(text=final_output)]
                )
            )

            return trace_logger.export(), conversation_history

        else:
            tool_result = TOOLS[tool_name](**tool_args)

        print(f"📦 Result: {tool_result}")

        trace_logger.log_tool_call(tool_name, tool_args, tool_result)

        conversation_history.append(
            types.Content(
                role="model",
                parts=[types.Part(function_call=function_call)]
            )
        )

        conversation_history.append(
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        function_response=types.FunctionResponse(
                            name=tool_name,
                            response=tool_result,
                        )
                    )
                ],
            )
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=conversation_history,
            config=config,
        )

        function_call = extract_function_call(response)

    final_output = response.text

    conversation_history.append(
        types.Content(
            role="model",
            parts=[types.Part(text=final_output)]
        )
    )

    print("\n🧾 FINAL OUTPUT:")
    print(final_output)

    print("\n📊 TRACE:")
    print(trace_logger.export())

    return trace_logger.export(), conversation_history


if __name__ == "__main__":
    conversation_history = []

    while True:
        q = input("\nEnter query (exit to stop): ")
        if q.lower() == "exit":
            break

        _, conversation_history = run_agent(q, conversation_history)