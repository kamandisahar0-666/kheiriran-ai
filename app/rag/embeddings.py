from fastembed import TextEmbedding
from fastembed.common.model_description import (
    PoolingType,
    ModelSource,
)


MODEL_NAME = "intfloat/multilingual-e5-small"
EMBEDDING_DIMENSION = 384


TextEmbedding.add_custom_model(
    model=MODEL_NAME,
    pooling=PoolingType.MEAN,
    normalization=True,
    sources=ModelSource(
        hf=MODEL_NAME
    ),
    dim=EMBEDDING_DIMENSION,
    model_file="onnx/model.onnx",
)


model = TextEmbedding(
    model_name=MODEL_NAME
)


def create_passage_embedding(text: str) -> list[float]:
    if not text.strip():
        raise ValueError("Cannot embed empty text")

    prepared_text = f"passage: {text}"

    embedding = list(
        model.embed([prepared_text])
    )[0]

    return embedding.tolist()


def create_query_embedding(text: str) -> list[float]:
    if not text.strip():
        raise ValueError("Cannot embed empty query")

    prepared_text = f"query: {text}"

    embedding = list(
        model.embed([prepared_text])
    )[0]

    return embedding.tolist()