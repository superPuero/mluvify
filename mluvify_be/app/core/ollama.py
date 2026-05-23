from typing import Annotated
from ollama import AsyncClient
from fastapi import HTTPException, Depends

from app.core.settings import settings

class OllamaServiceManager:
    def __init__(self) -> None:
        self._client: AsyncClient | None = None
    
    async def startup(self) -> None:
        self._client = AsyncClient(host=settings.ollama.host)
    
    async def shutdown(self) -> None:
        self._client = None
    
    async def __call__(self) -> AsyncClient:
        if self._client is None:
            raise HTTPException(status_code=503, detail="AI Service is currently down")
        return self._client


ollama_service: OllamaServiceManager = OllamaServiceManager()


OllamaDep = Annotated[AsyncClient, Depends(ollama_service)]
