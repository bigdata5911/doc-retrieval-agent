import sys
sys.path.insert(0, "./")
from dotenv import load_dotenv
load_dotenv()

from app.ai.tools.faq_tool import get_faq_tool

tool = get_faq_tool()

print(tool.invoke("What is the return policy?"))