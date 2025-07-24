import asyncio
from httpx import AsyncClient, Timeout

async def test_chat_endpoint():
    timeout = Timeout(60.0)  # 60 seconds, adjust as needed
    async with AsyncClient(base_url="http://localhost:8000", timeout=timeout) as ac:
        response = await ac.post("/chat", json={"message": "What is the return policy?"})
        print(f"Status code: {response.status_code}")
        # SSE response: collect streamed data
        chunks = []
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                chunks.append(line[len("data: "):])
        print("\n".join(chunks))

if __name__ == "__main__":
    asyncio.run(test_chat_endpoint())