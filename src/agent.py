import json
from openai import OpenAI

from tools import TOOLS
from prompts import SYSTEM_PROMPT
from trace import TraceLogger
from config import MODEL_NAME

client = OpenAI()


def run_agent(user_input):
    trace_logger = TraceLogger()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=[],
        tool_choice="auto"
    )

    msg = response.choices[0].message

    print("\n🧠 AGENT START")
    print("User:", user_input)

    # TOOL LOOP
    while hasattr(msg, "tool_calls") and msg.tool_calls:

        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            print(f"\n🔧 Tool: {name} | Args: {args}")

            result = TOOLS[name](**args)

            trace_logger.log_tool_call(name, args, result)

            messages.append(msg)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=[],
            tool_choice="auto"
        )

        msg = response.choices[0].message

    print("\n🧾 FINAL OUTPUT:")
    print(msg.content)

    print("\n📊 TRACE:")
    print(trace_logger.export())

    return trace_logger.export()


if __name__ == "__main__":
    while True:
        q = input("\nEnter query (exit to stop): ")
        if q == "exit":
            break
        run_agent(q)
