import asyncio
from typing import Annotated
from fastapi import HTTPException, Depends
from faster_whisper import WhisperModel

from app.core.settings import settings

class WhisperServiceManager:
    def __init__(self) -> None:
        self._model: WhisperModel | None = None
    
    async def startup(self) -> None:
        self._model = await asyncio.to_thread(
            WhisperModel,
            settings.whisper.model_size,
            device=settings.whisper.device,
            compute_type=settings.whisper.compute_type,
        )
    
    async def shutdown(self) -> None:
        self._model = None
    
    async def __call__(self) -> WhisperModel:
        if self._model is None:
            raise HTTPException(status_code=503, detail="Transcription service is down")
        return self._model


whisper_service: WhisperServiceManager = WhisperServiceManager()

WhisperDep = Annotated[WhisperServiceManager, Depends(whisper_service)]
