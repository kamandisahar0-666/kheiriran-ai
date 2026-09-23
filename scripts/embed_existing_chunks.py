from sqlalchemy import text

from app.db.database import engine
from app.rag.embeddings import create_passage_embedding


def vector_to_postgres(values: list[float]) -> str:
    return "[" + ",".join(str(value) for value in values) + "]"


def embed_existing_chunks():
    with engine.begin() as connection:

        # فقط Chunkهایی که هنوز embedding ندارند
        chunks = connection.execute(
            text("""
                SELECT id, content, chunk_index
                FROM chunks
                WHERE embedding IS NULL
                ORDER BY created_at ASC
            """)
        ).mappings().all()

        print(f"Chunks without embedding: {len(chunks)}")

        if not chunks:
            print("Nothing to embed.")
            return

        for index, chunk in enumerate(chunks, start=1):

            print(
                f"Embedding chunk "
                f"{index}/{len(chunks)} "
                f"(chunk_index={chunk['chunk_index']})"
            )

            embedding = create_passage_embedding(
                chunk["content"]
            )

            if len(embedding) != 384:
                raise RuntimeError(
                    f"Unexpected embedding dimension: "
                    f"{len(embedding)}"
                )

            connection.execute(
                text("""
                    UPDATE chunks
                    SET embedding = CAST(:embedding AS vector)
                    WHERE id = :chunk_id
                """),
                {
                    "embedding": vector_to_postgres(embedding),
                    "chunk_id": chunk["id"],
                }
            )

        print("Embedding process completed successfully.")


if __name__ == "__main__":
    embed_existing_chunks()