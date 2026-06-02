from django.conf import settings
from openai import AsyncOpenAI
from typing import AsyncGenerator

SYSTEM_PROMPT = ""


async def stream_response(message: str) -> AsyncGenerator[str, None]:
    client = AsyncOpenAI(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
    )
    stream = await client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
        stream=True,
    )
    async for chunk in stream:
        token = chunk.choices[0].delta.content
        if token:
            yield token