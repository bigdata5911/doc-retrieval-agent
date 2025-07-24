import sys
sys.path.insert(0, "./")
from dotenv import load_dotenv
load_dotenv()

from app.ai.agent import faq_agent
import pprint

def print_result(query):
    print(f"Query: {query}")
    output = faq_agent.invoke({"messages": [{"role": "user", "content": query}]})
    pprint.pprint(output)
    print("-" * 40)

print_result("What is the return policy?")
# print_result("How do I contact support?")
# print_result("Where are you located?") 