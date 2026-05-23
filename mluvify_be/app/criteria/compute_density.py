from lexicalrichness import LexicalRichness
from app.core.context import CriteriaContext, MessageEntry
from pydantic import BaseModel

WEIGHTS = {
    "NOUN": 1.2,
    "VERB": 1.5,
    "ADJ": 1.0,
    "ADV": 0.8,
    "PRON": 0.2,
    "AUX": 0.1,
    "ADP": 0.0
}

def compute_weighted_idea_density(criteria_context: CriteriaContext, message_entry: MessageEntry) -> float:
    total_weight = 0
    total_tokens = 0

    for token in message_entry.sentences:

            if token == "PUNCT":
                continue

            upos = token

            total_tokens += 1
            total_weight += WEIGHTS.get(upos, 0)

    return total_weight / max(total_tokens, 1)