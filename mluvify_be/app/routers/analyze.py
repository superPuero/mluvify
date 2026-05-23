from fastapi import APIRouter
from app.utils.deps import AudioFile
from app.core.whisper import WhisperDep, WhisperModel
from app.core.ollama import OllamaDep
from app.core.spacy import SpacyModelDep
from app.core.context import CriteriaContextDep, MessageEntry

import io

router = APIRouter(
    prefix="/analyze",
    tags=["Analyze"],
)

@router.get("/semantic")
async def analyze_semantic(ollama: OllamaDep, wisper: WhisperDep, spacy_model: SpacyModelDep, criteria_context: CriteriaContextDep, file: AudioFile):     
    wisper_model: WhisperModel = await wisper()
    file_bytes = await file.read()
    audio_stream = io.BytesIO(file_bytes)
    
    segment_gen, info = wisper_model.transcribe(
        audio_stream, 
        language="cs", 
        word_timestamps=True
    )
    
    segments = list(segment_gen)
    
    text_from_audio = "".join([segment.text for segment in segments])
    sentences_list = [segment.text.strip() for segment in segments if len(segment.text.strip()) > 0]
    
    message_entry: MessageEntry = MessageEntry(text=text_from_audio, sentences=sentences_list, parts_and_lemmas=spacy_model.into_part_and_lemmas(text_from_audio))
    context.criterial += criteria_1_eval(context, message_entry)               
    pass


@router.get("/rithoric", deprecated=True)
async def analyze_rithoric():
    pass
