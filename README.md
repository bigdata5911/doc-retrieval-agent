# Offline Chatbot App

This app is an offline AI chatbot that answers queries from:

- A folder of 5 .txt FAQ documents (for FAQ search)
- A .csv file of monthly sales (columns: Date, Product, Sales; for sales analytics)

## Features

- LangChain agent with Supervisor for tool routing (FAQ and sales)
- FAQ search using OpenAI embeddings and vector search
- Sales data Q&A using SQL over a SQLite database (automatically loaded from CSV)
- FastAPI backend with streaming responses (SSE)
- Uses OpenAI API for both LLM and embeddings (set your OPENAI_API_KEY)
- All test files are in the `test/` directory

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your OpenAI API key in your environment or add it into env file:
   ```bash
   export OPENAI_API_KEY=sk-...
   ```
3. Place your 5 FAQ `.txt` files in `data/faqs/`.
4. Place your sales data in `data/sales.csv` (columns: Date, Product, Sales).
5. Run the backend:
   ```bash
   uvicorn app.main:app --reload
   ```

## Usage

- Send POST requests to `/chat` with `{ "message": "your question" }`.
- Responses are streamed back as text chunks (SSE).
- The agent will automatically route questions to the FAQ or sales SQL agent as appropriate.

## Testing

- All test files are in the `test/` directory.
- To run a test manually:
  ```bash
  python test/test_faq_agent.py
  python test/test_sales_agent.py
  python test/test_faq_tool.py
  python test/test_fastapi_chat.py
  ```
- The FastAPI chat endpoint can be tested with `test/test_fastapi_chat.py` (streams SSE responses).

---
