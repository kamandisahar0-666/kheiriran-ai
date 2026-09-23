from pathlib import Path

from sqlalchemy import text

from app.db.database import engine
from app.rag.chunker import chunk_text


SAMPLE_FILE = Path("data/samples/sample.txt")


def ingest():
    raw_text = SAMPLE_FILE.read_text(encoding="utf-8")

    chunks = chunk_text(raw_text)

    print(f"Total chunks: {len(chunks)}")

    with engine.begin() as connection:

        # 1. Source
        source_result = connection.execute(
            text("""
                INSERT INTO sources (
                    title,
                    url,
                    source_type
                )
                VALUES (
                    :title,
                    :url,
                    :source_type
                )
                RETURNING id
            """),
            {
                "title": "منبع آزمایشی خیر ایران",
                "url": "https://kheir.ir",
                "source_type": "manual"
            }
        )

        source_id = source_result.scalar_one()

        # 2. Document
        document_result = connection.execute(
            text("""
                INSERT INTO documents (
                    source_id,
                    title,
                    content
                )
                VALUES (
                    :source_id,
                    :title,
                    :content
                )
                RETURNING id
            """),
            {
                "source_id": source_id,
                "title": "سند آزمایشی خیر ایران",
                "content": raw_text
            }
        )

        document_id = document_result.scalar_one()

        # 3. Chunks
        for chunk in chunks:
            connection.execute(
                text("""
                    INSERT INTO chunks (
                        document_id,
                        source_id,
                        chunk_index,
                        content,
                        token_count
                    )
                    VALUES (
                        :document_id,
                        :source_id,
                        :chunk_index,
                        :content,
                        :token_count
                    )
                """),
                {
                    "document_id": document_id,
                    "source_id": source_id,
                    "chunk_index": chunk["chunk_index"],
                    "content": chunk["content"],
                    "token_count": chunk["token_count"]
                }
            )

    print("Ingestion completed successfully.")


if __name__ == "__main__":
    ingest()