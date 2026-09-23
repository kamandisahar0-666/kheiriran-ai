import os

import httpx
from dotenv import load_dotenv


load_dotenv()


OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://192.168.66.6:11434",
).rstrip("/")

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3:1.7b",
)


SYSTEM_PROMPT = """
تو دستیار هوشمند خیر ایران هستی.

وظیفه تو این است که فقط بر اساس اطلاعاتی که
در بخش CONTEXT در اختیارت قرار می‌گیرد پاسخ بدهی.

قوانین:
1. فقط از CONTEXT استفاده کن.
2. از دانش عمومی خودت برای تکمیل پاسخ استفاده نکن.
3. اگر پاسخ در CONTEXT وجود ندارد، بگو:
   «اطلاعات کافی در منابع موجود خیر ایران پیدا نشد.»
4. اطلاعات حدسی یا ساختگی تولید نکن.
5. پاسخ را فارسی، روان، واضح و مختصر بنویس.
6. اگر اطلاعات چند منبع مرتبط بود، آن‌ها را ترکیب کن.
7. درباره RAG، Vector Database، Embedding یا فرآیند داخلی سیستم
   با کاربر صحبت نکن.
"""


async def generate_answer(
    question: str,
    context: str,
) -> dict:

    user_prompt = f"""
CONTEXT:
==============================

{context}

==============================

QUESTION:
{question}

فقط بر اساس CONTEXT بالا پاسخ بده.
"""

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        "stream": False,
        "think": False,
        "options": {
            "temperature": 0.2,
        },
    }

    async with httpx.AsyncClient(
        timeout=120.0,
    ) as client:

        response = await client.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
        )

        response.raise_for_status()

        data = response.json()

    message = data.get(
        "message",
        {},
    )

    answer = message.get(
        "content",
        "",
    ).strip()

    return {
        "answer": answer,
        "model": data.get(
            "model",
            OLLAMA_MODEL,
        ),
        "prompt_tokens": data.get(
            "prompt_eval_count",
            0,
        ),
        "output_tokens": data.get(
            "eval_count",
            0,
        ),
    }