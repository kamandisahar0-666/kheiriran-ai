import tiktoken


ENCODING = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    return len(ENCODING.encode(text))


def chunk_text(
    text: str,
    chunk_size: int = 700,
    overlap: int = 80
) -> list[dict]:
    tokens = ENCODING.encode(text)

    chunks = []

    start = 0
    index = 0

    while start < len(tokens):
        end = start + chunk_size

        chunk_tokens = tokens[start:end]
        chunk_text_value = ENCODING.decode(chunk_tokens)

        chunks.append({
            "chunk_index": index,
            "content": chunk_text_value,
            "token_count": len(chunk_tokens)
        })

        index += 1

        if end >= len(tokens):
            break

        start = end - overlap

    return chunks