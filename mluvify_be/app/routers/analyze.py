from fastapi import APIRouter
from app.utils.deps import AudioFile

from app.core.ollama import OllamaDep
from app.core.whisper import whisper_model

router = APIRouter(
    prefix="/analyze",
    tags=["Analyze"],
)

@router.get("/semantic")
async def analyze_semantic(ollama: OllamaDep, file: AudioFile):            
    pass


@router.get("/rithoric", deprecated=True)
async def analyze_rithoric():
    pass
