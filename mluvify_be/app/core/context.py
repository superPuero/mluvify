from typing import Annotated
from fastapi import Depends
from ollama import AsyncClient
from faster_whisper import WhisperModel

from app.core.ollama import OllamaDep
from app.core.whisper import WhisperDep


class CriteriaContext:
    def __init__(self, ollama: AsyncClient, whisper: WhisperModel) -> None:
        self.ollama: AsyncClient = ollama
        self.whisper: WhisperModel = WhisperModel

        self.criterias: dict[str, list[float]] = {}


async def get_criteria_context(
    ollama: OllamaDep,
    whisper: WhisperDep,
):
    pass


# CriteriaContextDep = Annotated[CriteriaContext, Depends()]