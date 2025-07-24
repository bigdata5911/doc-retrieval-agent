from langchain.tools import Tool
from app.ai.utils import csv_to_sqlite, run_sql_query
import os
from langchain_openai import ChatOpenAI
import re

SALES_CSV_PATH = os.path.join(os.path.dirname(__file__), '../../../data/csv_files/sales.csv')
SALES_DB_PATH = os.path.join(os.path.dirname(__file__), '../../../data/csv_files/sales.db')
SALES_TABLE = "sales"
SALES_METADATA = (
    "The sales.csv file has columns: "
    "Date (YYYY-MM-DD, the date of the sale), "
    "Product (the product name, e.g., Widget, Gadget), "
    "Sales (integer, units sold)."
)

def ensure_db():
    if not os.path.exists(SALES_DB_PATH):
        csv_to_sqlite(SALES_CSV_PATH, SALES_DB_PATH, SALES_TABLE)

def parse_sql_query(response):
    # Handles both string and OpenAI message object
    if hasattr(response, 'content'):
        text = response.content
    else:
        text = str(response)
    # Remove markdown code block if present
    match = re.search(r"```sql\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Fallback: return the whole text
    return text.strip()

def get_sql_agent_tool():
    def sql_agent_func(query):
        ensure_db()
        from app.ai.agent import model
        prompt = (
            f"You are a helpful assistant. "
            f"The sales table has columns: Date (text), Product (text), Sales (integer). "
            f"Given the following user request, generate a valid SQLite SQL query to answer it. "
            f"Return ONLY the SQL query, nothing else.\n"
            f"User request: {query}"
        )
        response = model.invoke(prompt)
        print("Response: ", response)
        sql_query = parse_sql_query(response)
        print("SQL Query: ", sql_query)
        try:
            result = run_sql_query(SALES_DB_PATH, sql_query)
            return {"result": result, "sql": sql_query}
        except Exception as e:
            return {"error": str(e), "sql": sql_query}
    return Tool(
        name="sql_sales_agent",
        description=f"Useful for answering any question about sales data using SQL. {SALES_METADATA} Just ask in natural language.",
        func=sql_agent_func,
        return_direct=True,
    )
