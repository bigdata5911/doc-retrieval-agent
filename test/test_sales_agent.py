import sys
sys.path.insert(0, "./")
from dotenv import load_dotenv
load_dotenv()

from app.ai.agent import sales_agent
import pprint

def print_result(query):
    print(f"Query: {query}")
    output = sales_agent.invoke({"messages": [{"role": "user", "content": query}]})
    tool_result = None
    if isinstance(output, dict):
        messages = output.get("messages")
        if messages and isinstance(messages, list):
            for msg in reversed(messages):
                # Handle both dict and object message types
                if isinstance(msg, dict):
                    if msg.get("tool_call_id") or msg.get("tool_calls") or msg.get("tool_call"):
                        tool_result = msg.get("content") or msg.get("tool_call") or msg.get("tool_calls")
                        break
                else:
                    # Try to access as object attributes
                    if hasattr(msg, "tool_call_id") or hasattr(msg, "tool_calls") or hasattr(msg, "tool_call"):
                        tool_result = getattr(msg, "content", None) or getattr(msg, "tool_call", None) or getattr(msg, "tool_calls", None)
                        break
        if not tool_result:
            tool_result = output
    else:
        tool_result = output
    pprint.pprint(tool_result)
    print("-" * 40)

print_result("Total sales for Widget")
# print_result("Average sales for Gadget")
# print_result("How many sales records for Widget?")
# print_result("List all products")
# print_result("Show sales for Widget on 2024-06-01") 