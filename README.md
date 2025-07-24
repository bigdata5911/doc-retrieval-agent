# Offline Chatbot App

This app is an offline AI chatbot that answers queries from:

- A folder of 5 .txt FAQ documents
- A .csv file of monthly sales (columns: Date, Product, Sales)

## Features

- LangChain agent with Supervisor for tool routing
- FAQ search and sales data Q&A
- FastAPI backend with streaming responses (SSE)
- Uses OpenAI API for LLM (set your OPENAI_API_KEY)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
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

## Usage

- Send POST requests to `/chat` with `{ "message": "your question" }`.
- Responses are streamed back as text chunks.

---
