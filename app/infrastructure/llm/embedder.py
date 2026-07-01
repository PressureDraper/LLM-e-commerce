from app.config import settings
from app.infrastructure.llm.client import get_embedder


async def embed_text(text: str) -> list[float]:
    # generates embeddings for the given text using the cohere API
    # input_type="search_document" indexes products
    # input_type="search_query" for user queries in search module
    client = get_embedder()
    response = await client.embed(
        texts=[text],
        model=settings.COHERE_EMBED_MODEL,
        input_type="search_document",
        embedding_types=["float"]
    )
    return response.embeddings.float[0]
