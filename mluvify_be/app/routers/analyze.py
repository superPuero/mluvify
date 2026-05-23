import numpy as np
import io
from fastapi import APIRouter
from app.utils.deps import AudioFile
from app.core.whisper import WhisperDep, WhisperModel
from app.core.ollama import OllamaDep
from app.core.spacy import SpacyModelDep
from app.core.networkx import NetworkxDep
from app.core.context import CriteriaContextDep, MessageEntry, CriteriaContextData, CriteriaContext
from app.criteria.speech_graph import speech_graph_criteria, SpeechGraphData
from app.criteria.compute_density import compute_weighted_idea_density
from app.criteria.lexical_richness import LexicalRichnessData, get_lexical_metrics
from app.criteria.window_semantic_similarity import WindowSemantcSimilarityData, window_semantic_similarity_evaluate
from app.criteria.speech_rate import SpeechRateData, speech_rate_evaluate

def clamp(x, min_val=0.0, max_val=1.0):
    return max(min_val, min(x, max_val))


def norm_minmax(x, min_val, max_val):
    x = clamp(x, min_val, max_val)
    return (x - min_val) / (max_val - min_val + 1e-8)


def norm_log(x, max_ref):
    return np.log(1 + x) / np.log(1 + max_ref)


def exp_penalty(count, severity=1.0, k=0.7):
    return severity * (1 - np.exp(-k * count))



def compute_scores(
    criteria_context: CriteriaContext,
    lex_richness: LexicalRichnessData, 
    window_semantics_sim: WindowSemantcSimilarityData, 
    speech_rate_data: SpeechRateData,
    speech_graph_data: SpeechGraphData
    ):

    """
    metrics = dict with already computed values
    """

    # -------------------------
    # LEXICAL RICHNESS
    # -------------------------
    lexical = np.mean([
        1 - norm_minmax(lex_richness.data["ttr"], 0.2, 0.9),
        1 - norm_minmax(lex_richness.data["mattr"], 0.3, 0.95),
        1 - norm_minmax(lex_richness.data["mtld"], 5, 120),
        1 - norm_minmax(lex_richness.data["hdd"], 0.4, 0.9),
    ])


    # -------------------------
    # IDEA DENSITY
    # -------------------------
    # idea_density = 1 - norm_minmax(weighted_density, 0.0, 1.0)

    repetition = exp_penalty(window_semantics_sim.data["count_repeated_words"], severity=1.2, k=0.8)

    fluency = np.mean([
        1 - norm_minmax(speech_rate_data.data["words_per_second"], 0.8, 3.0),
        1 - norm_minmax(speech_rate_data.data["syllables_per_second"], 1.5, 5.0),
        norm_log(speech_rate_data.data["pause_count"], 30),
        norm_minmax(speech_rate_data.data["silence_ratio"], 0.0, 0.5),
        norm_minmax(speech_rate_data.data["average_pause_duration"], 0.0, 2.0),
    ])



    graph = np.mean([
        norm_minmax(speech_graph_data.data["clustering_coeff"], 0.0, 0.3),
        norm_log(speech_graph_data.data["l1_loops"], 15),
        norm_log(speech_graph_data.data["l2_loops"], 10),
        norm_minmax(speech_graph_data.data["density"], 0.0, 0.1),
    ])



    final_score = (
        0.35 * lexical +
        0.25 * graph +
        0.20 * repetition +
        0.15 * fluency
    )
    
    if 'FlowCriteria' in criteria_context.criteria_data.criterias:
        criteria_context.criteria_data.criterias['FlowCriteria'].append(graph)
    else:
        criteria_context.criteria_data.criterias['FlowCriteria'] = [graph]

    if 'LexicalAnalysis' in criteria_context.criteria_data.criterias:
        criteria_context.criteria_data.criterias['LexicalAnalysis'].append(lexical)
    else:
        criteria_context.criteria_data.criterias['LexicalAnalysis'] = [lexical]

    if 'Repetitions' in criteria_context.criteria_data.criterias:
        criteria_context.criteria_data.criterias['Repetitions'].append(repetition)
    else:
        criteria_context.criteria_data.criterias['Repetitions'] = [repetition]

    if 'Fluency' in criteria_context.criteria_data.criterias:
        criteria_context.criteria_data.criterias['Fluency'].append(fluency)
    else:
        criteria_context.criteria_data.criterias['Fluency'] = [fluency]

    score = clamp(final_score)

    if 'FinalScore' in criteria_context.criteria_data.criterias:
        criteria_context.criteria_data.criterias['FinalScore'].append(score)
    else:
        criteria_context.criteria_data.criterias['FinalScore'] = [score]

    if 'RiskLevel' in criteria_context.criteria_data.criterias:
        criteria_context.criteria_data.criterias['RiskLevel'].append(final_score)
    else:
        criteria_context.criteria_data.criterias['RiskLevel'] = [final_score]

def classify_risk(score):
    if score < 0.35:
        return "healthy"
    elif score < 0.6:
        return "mild impairment"
    else:
        return "high impairment"   

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

    criteria_context.criteria_data.all_messages.append(text_from_audio);
    criteria_context.llm_msg.append( {"role": "user", "content": text_from_audio} );
    
    compute_scores(
        criteria_context=criteria_context, 
        lex_richness=get_lexical_metrics(criteria_context=criteria_context, message_entry=message_entry),
        window_semantics_sim=window_semantic_similarity_evaluate(criteria_context=criteria_context, message_entry=message_entry),
        speech_rate_data=speech_rate_evaluate(segments=segments, criteria_context=criteria_context, message_entry=message_entry),
        speech_graph_data=speech_graph_criteria(criteria_context=criteria_context, graph_model=graph_model, message_entry=message_entry)           
    );    
  
    response = await ollama.chat(
        "llama3.1",
        messages=criteria_context.llm_msg
    )

    criteria_context.criteria_data.all_messages.append(response["message"]["content"])
    criteria_context.llm_msg.append(response["message"])
  
    return criteria_context.criteria_data


@router.get("/rithoric", deprecated=True)
async def analyze_rithoric():
    pass
