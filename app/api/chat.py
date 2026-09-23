import httpx

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.rag.retriever import search_chunks
from app.services.llm import generate_answer


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):

    message: str = Field(
        min_length=2,
        max_length=1000,
        examples=[
            "خیر ایران چه خدماتی ارائه می‌دهد؟"
        ]
    )


@router.post("")
async def chat(request: ChatRequest):

    try:

        # -------------------------
        # 1. Semantic Search
        # -------------------------

        search_results = search_chunks(
            query=request.message,
            limit=5
        )

        # -------------------------
        # 2. Filter weak results
        # -------------------------

        relevant_results = []

        for result in search_results:

            similarity = float(
                result["similarity"]
            )

            if similarity >= 0.55:
                relevant_results.append(
                    result
                )

        # -------------------------
        # 3. No valid source
        # -------------------------

        if not relevant_results:

            return {
                "answer": (
                    "اطلاعات کافی در منابع موجود "
                    "خیر ایران پیدا نشد."
                ),

                "sources": [],

                "model": None,

                "usage": {
                    "input_tokens": 0,
                    "output_tokens": 0
                }
            }

        # -------------------------
        # 4. Build RAG Context
        # -------------------------

        context_parts = []

        for index, result in enumerate(
            relevant_results,
            start=1
        ):

            context_parts.append(
                f"""
منبع {index}

عنوان:
{result["source_title"]}

آدرس:
{result["source_url"]}

محتوا:
{result["content"]}
"""
            )

        context = "\n\n".join(
            context_parts
        )

        # -------------------------
        # 5. Call Ollama
        # -------------------------

        llm_result = await generate_answer(
            question=request.message,
            context=context
        )

        # -------------------------
        # 6. Build source list
        # -------------------------

        sources = []

        seen_sources = set()

        for result in relevant_results:

            key = (
                result["source_title"],
                result["source_url"]
            )

            if key in seen_sources:
                continue

            seen_sources.add(key)

            sources.append({
                "title":
                    result["source_title"],

                "url":
                    result["source_url"],

                "similarity":
                    round(
                        float(
                            result["similarity"]
                        ),
                        4
                    )
            })

        # -------------------------
        # 7. Final response
        # -------------------------

        return {

            "answer":
                llm_result["answer"],

            "sources":
                sources,

            "model":
                llm_result["model"],

            "usage": {

                "input_tokens":
                    llm_result[
                        "prompt_tokens"
                    ],

                "output_tokens":
                    llm_result[
                        "output_tokens"
                    ]
            }
        }

    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Ollama connection error: {exc}"
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )