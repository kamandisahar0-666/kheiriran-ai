from sqlalchemy import text

from app.db.database import engine
from app.rag.embeddings import create_query_embedding


def vector_to_postgres(values: list[float]) -> str:
    return "[" + ",".join(str(value) for value in values) + "]"


def search_chunks(query: str, limit: int = 5) -> list[dict]:
    query_embedding = create_query_embedding(query)

    if len(query_embedding) != 384:
        raise RuntimeError(
            f"Unexpected query embedding dimension: {len(query_embedding)}"
        )

    query_vector = vector_to_postgres(query_embedding)

    with engine.connect() as connection:
        rows = connection.execute(
            text("""
                SELECT
                    c.id,
                    c.chunk_index,
                    c.content,
                    c.token_count,
                    s.title AS source_title,
                    s.url AS source_url,
                    1 - (c.embedding <=> CAST(:query_vector AS vector))
                        AS similarity
                FROM chunks c
                JOIN sources s
                    ON s.id = c.source_id
                WHERE c.embedding IS NOT NULL
                ORDER BY
                    c.embedding <=> CAST(:query_vector AS vector)
                LIMIT :limit
            """),
            {
                "query_vector": query_vector,
                "limit": limit
            }
        ).mappings().all()

    return [dict(row) for row in rows]