from app.rag.retriever import search_chunks


def main():
    query = "خیر ایران چه خدماتی ارائه می‌دهد؟"

    results = search_chunks(
        query=query,
        limit=5
    )

    print(f"Query: {query}")
    print(f"Results: {len(results)}")
    print("-" * 80)

    for index, result in enumerate(results, start=1):
        print(f"Result #{index}")
        print(
            "Similarity:",
            round(float(result["similarity"]), 4)
        )
        print(
            "Source:",
            result["source_title"]
        )
        print(
            "URL:",
            result["source_url"]
        )
        print(
            "Chunk index:",
            result["chunk_index"]
        )
        print("Content:")
        print(result["content"])
        print("-" * 80)


if __name__ == "__main__":
    main()