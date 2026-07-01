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

async def embed_query(text: str) -> list[float]:
    # generates embeddings from a user query
    #uses different input_type="search_query" for better accuracy in search results
    client = get_embedder()
    response = await client.embed(
        texts=[text],
        model=settings.COHERE_EMBED_MODEL,
        input_type="search_query",
        embedding_types=["float"]
    )
    return response.embeddings.float[0]

async def embed_batch(texts: list[str]) -> list[list[float]]:
    #generates embeddings from multiple texts in a single call
    client = get_embedder()
    
    #cohere free tier limit: 96 texts per request
    BATCH_SIZE = 96
    all_embeddings: list[list[float]] = []

    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]
        response = await client.embed(
            texts=batch,
            model=settings.COHERE_EMBED_MODEL,
            input_type="search_document",
            embedding_types=["float"]
        )
        all_embeddings.extend(response.embeddings.float)
    
    return all_embeddings

