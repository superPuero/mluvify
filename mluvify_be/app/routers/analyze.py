from fastapi import APIRouter
from app.utils.deps import AudioFile

from app.core.ollama import OllamaDep

router = APIRouter(
    prefix="/analyze",
    tags=["Analyze"],
)


@router.get("/semantic")
async def analyze_semantic(ollama: OllamaDep, file: AudioFile):
    return {"test": "test"}


@router.get("/rithoric", deprecated=True)
async def analyze_rithoric():
    pass
