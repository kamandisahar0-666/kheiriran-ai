from app.rag.embeddings import (
    create_passage_embedding,
    create_query_embedding,
)


def main():
    passage = """
    خیر ایران در زمینه توسعه زیرساخت‌های نیکوکاری
    و ارائه خدمات به موسسات خیریه فعالیت می‌کند.
    """

    query = "خیر ایران چه خدماتی ارائه می‌دهد؟"

    passage_embedding = create_passage_embedding(
        passage
    )

    query_embedding = create_query_embedding(
        query
    )

    print("Local embedding created successfully.")

    print(
        "Passage dimensions:",
        len(passage_embedding)
    )

    print(
        "Query dimensions:",
        len(query_embedding)
    )

    print(
        "First 10 passage values:"
    )

    print(
        passage_embedding[:10]
    )


if __name__ == "__main__":
    main()