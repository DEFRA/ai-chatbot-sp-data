from app.common.bedrock import AbstractEmbeddingService

from httpx import AsyncClient


def ingest_url(
        http_client: AsyncClient,
        embedding_service: AbstractEmbeddingService,
        url: str
    ):

    content = "Simulated content from the URL."

    embeddings = embedding_service.generate_embeddings(content)

    return embeddings
    
    