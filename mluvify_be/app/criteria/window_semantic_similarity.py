from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from lexicalrichness import LexicalRichness
from app.core.context import CriteriaContext, MessageEntry
from pydantic import BaseModel

class WindowSemantcSimilarityData:
    def __init__(self):
        self.data: dict[str, any] = {}

def window_semantic_similarity_evaluate(criteria_context: CriteriaContext, message_entry: MessageEntry) -> WindowSemantcSimilarityData:    
   
    def words_repeated(lemmas):
        if not lemmas:
            return 0.0
        unikatni_slova = set(lemmas)
        redundance_slov = 1.0 - (len(unikatni_slova) / len(lemmas))
        return redundance_slov



    count_repeated_words = words_repeated(message_entry.parts_and_lemmas.lemmas)

    data = WindowSemantcSimilarityData();
    data.data = {
        "count_repeated_words": count_repeated_words
    }

    return data

