import cohere
from app.config import settings

_client = cohere.AsyncClient | None = None


def get_embedder() -> cohere.AsyncClient:
    global _client
    if _client is None:
        _client = cohere.AsyncClient(api_key=settings.COHERE_API_KEY)
        return _client
