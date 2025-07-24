# agent.py
# LangChain agent setup for FAQ and sales tools 
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from app.ai.tools.faq_tool import get_faq_tool
from app.ai.tools.sales_tool import get_sql_agent_tool
from dotenv import load_dotenv

load_dotenv()

# --- LLM Setup ---
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# --- Create Specialized Agents ---
faq_agent = create_react_agent(
    model,
    tools=[get_faq_tool()],
    name="faq_agent",
    prompt="You are an FAQ expert. Use the FAQ Search tool to answer questions from the FAQ documents."
)

sales_agent = create_react_agent(
    model,
    tools=[get_sql_agent_tool()],
    name="sales_agent",
    prompt="You are a sales data expert. Use the SQL Sales Agent tool to answer any question about sales from the sales database."
)

# --- Supervisor Agent ---
supervisor_prompt = (
    "You are a smart supervisor. Route FAQ questions to faq_agent and sales questions to sales_agent. "
    "Choose the most appropriate agent based on the user's input."
)
supervisor = create_supervisor(
    [faq_agent, sales_agent],
    model=model,
    prompt=supervisor_prompt,
    output_mode="last_message"
).compile()

def get_supervisor():
    return supervisor 