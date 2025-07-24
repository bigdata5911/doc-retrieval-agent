# main.py
# FastAPI backend for streaming chat 
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from app.ai.agent import get_supervisor

app = FastAPI()
supervisor = get_supervisor()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data["message"]

    async def event_generator():
        # The workflow returns a list of messages; stream the content
        result = supervisor.invoke({
            "messages": [{"role": "user", "content": user_message}]
        })
        yield {"data": result["messages"][-1].content}
        # for m in result["messages"]:
        #     print(m)
        #     yield {"data": m.content}

    return EventSourceResponse(event_generator()) 