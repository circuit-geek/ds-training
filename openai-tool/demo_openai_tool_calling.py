import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import json

load_dotenv()

llm_client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_TOKEN"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("ENDPOINT")
)
deployment_name = os.getenv("DEPLOYMENT")

################### Using JSON structured OpenAI tool calling ##################

def add_nums(a, b):
    return a + b

def sub_nums(a, b):
    if a < b:
        return b - a
    else:
        return a - b

def mul_nums(a, b):
    return a * b

def div_nums(a, b):
    return a//b

def get_tool_response():
    messages = [{
        "role": "user",
        "content": "I want to know the following calculations, what is 5 + 3? what is 10 - 2? and what is 8 * 3?"
    }]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "add_nums",
                "description": "Returns the sum of two numbers",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number"},
                        "b": {"type": "number"}
                    },
                    "required": ["a", "b"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "sub_nums",
                "description": "Returns the difference of two numbers",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number"},
                        "b": {"type": "number"}
                    },
                    "required": ["a", "b"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "mul_nums",
                "description": "Returns the product of two numbers",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number"},
                        "b": {"type": "number"}
                    },
                    "required": ["a", "b"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "div_nums",
                "description": "Returns the division result of two numbers",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number"},
                        "b": {"type": "number"}
                    },
                    "required": ["a", "b"],
                },
            }
        }
    ]

    response = llm_client.chat.completions.create(
        model = deployment_name,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    tool_response = response.choices[0].message
    messages.append(tool_response)
    print(messages)

    if tool_response.tool_calls:
        for tool_call in tool_response.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            if tool_name == "add_nums":
                response = add_nums(
                    a = tool_args.get("a"),
                    b = tool_args.get("b")
                )

            elif tool_name == "sub_nums":
                response = sub_nums(
                    a = tool_args.get("a"),
                    b = tool_args.get("b")
                )

            elif tool_name == "mul_nums":
                response = mul_nums(
                    a = tool_args.get("a"),
                    b = tool_args.get("b")
                )

            elif tool_name == "div_nums":
                response = div_nums(
                    a = tool_args.get("a"),
                    b = tool_args.get("b")
                )

            else:
                response = json.dumps({"error": "Unknown function"})

            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": tool_name,
                "content": str(response)
            })

    else:
        print("No tool calls found")

    chat_response = llm_client.chat.completions.create(
        model = deployment_name,
        messages = messages
    )

    final_response = chat_response.choices[0].message.content
    print(final_response)

get_tool_response()