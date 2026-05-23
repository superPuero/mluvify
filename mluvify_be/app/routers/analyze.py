import io
from fastapi import APIRouter
from app.utils.deps import AudioFile
from app.core.whisper import WhisperDep, WhisperModel
from app.core.ollama import OllamaDep
from app.core.spacy import SpacyModelDep
from app.core.networkx import NetworkxDep
from app.core.context import CriteriaContextDep, MessageEntry, CriteriaContextData
from app.criteria.speech_graph import speech_graph_criteria


router = APIRouter(
    prefix="/analyze",
    tags=["Analyze"],
)


@router.post("/semantic")
async def analyze_semantic(
        ollama: OllamaDep, 
        wisper: WhisperDep, 
        graph_model: NetworkxDep, 
        spacy_model: SpacyModelDep, 
        criteria_context: CriteriaContextDep, 
        file: AudioFile
    ) -> CriteriaContextData:     
    file_bytes = await file.read()
    audio_stream = io.BytesIO(file_bytes)
    
    segment_gen, info = wisper.transcribe(
        audio_stream, 
        language="cs", 
        word_timestamps=True
    )
    
    segments = list(segment_gen)
    
    text_from_audio = "".join([segment.text for segment in segments])
    sentences_list = [segment.text.strip() for segment in segments if len(segment.text.strip()) > 0]
    
    message_entry: MessageEntry = MessageEntry(text=text_from_audio, sentences=sentences_list, parts_and_lemmas=spacy_model.into_part_and_lemmas(text_from_audio))
    
    new_criteria_value = speech_graph_criteria(
        criteria_context=criteria_context, 
        graph_model=graph_model, 
        message_entry=message_entry
    )

    if 'FlowCriteria' in criteria_context.criteria_data.criterias:
        criteria_context.criteria_data.criterias['FlowCriteria'].append(new_criteria_value)
    else:
        criteria_context.criteria_data.criterias['FlowCriteria'] = [new_criteria_value]

    return criteria_context.criteria_data


@router.get("/rithoric", deprecated=True)
async def analyze_rithoric():
    pass
