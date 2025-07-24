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
    prompt=(
        "You are an FAQ expert. Use the FAQ Search tool to answer questions ONLY from the FAQ documents. "
        "Always quote or summarize the most relevant answer from the documentation. "
        "Do NOT use general knowledge or make up answers. If the answer is not found in the documentation, say 'I could not find an answer in the FAQ documents.'"
    )
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
    "Choose the most appropriate agent based on the user's input. "
    "When you respond to the user, ONLY return the final answer in clear, natural language. "
    "For FAQ questions, the answer MUST be based on the FAQ documentation, not general knowledge. "
    "Do NOT include any internal routing, tool call details, agent transfer messages, or JSON. "
    "Your response should be concise and user-friendly, as if you are directly answering the user's question."
)
supervisor = create_supervisor(
    [faq_agent, sales_agent],
    model=model,
    prompt=supervisor_prompt,
    output_mode="last_message"
).compile()

def get_supervisor():
    return supervisor 