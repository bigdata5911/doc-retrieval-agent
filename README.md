# Document Retrieval Agent App

This app is a document-grounded AI chatbot that answers queries from:

- A folder of 5 .txt FAQ documents (for FAQ search)
- A .csv file of monthly sales (columns: Date, Product, Sales; for sales analytics)

## Features

- LangChain agent with Supervisor for tool routing (FAQ and sales)
- **FAQ agent always answers directly from the FAQ documentation, never from general LLM knowledge**
- FAQ search using OpenAI embeddings and vector search
- Sales data Q&A using SQL over a SQLite database (automatically loaded from CSV)
- FastAPI backend with streaming responses (SSE)
- Streamlit chat UI for interactive chat (port 8501)
- Uses OpenAI API for both LLM and embeddings (set your OPENAI_API_KEY)
- All test files are in the `test/` directory

## Setup (Local)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install streamlit sseclient
   ```
2. Set your OpenAI API key in your environment:
   ```bash
   export OPENAI_API_KEY=sk-...
   ```
3. Place your 5 FAQ `.txt` files in `data/faqs/`.
4. Place your sales data in `data/sales.csv` (columns: Date, Product, Sales).
5. Run the backend:
   ```bash
   uvicorn app.main:app --reload
   ```
6. Run the Streamlit chat UI:
   ```bash
   streamlit run app/streamlit_chat.py
   ```

## Docker Compose Deployment

1. Add your `OPENAI_API_KEY` to a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=sk-...
   ```
2. Build and start both backend and UI:
   ```bash
   docker-compose up --build
   ```
3. Access:
   - FastAPI backend: [http://localhost:8000](http://localhost:8000)
   - Streamlit chat UI: [http://localhost:8501](http://localhost:8501)
   - The Streamlit UI is preconfigured to use the backend at `http://app:8000/chat` (Docker Compose networking).

## Usage

- Send POST requests to `/chat` with `{ "message": "your question" }`.
- Responses are streamed back as text chunks (SSE).
- The agent will automatically route questions to the FAQ or sales SQL agent as appropriate.
- **FAQ answers are always grounded in your documentation. If no answer is found, the agent will say so.**

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
