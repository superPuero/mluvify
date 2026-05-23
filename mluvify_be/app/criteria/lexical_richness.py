from lexicalrichness import LexicalRichness
from app.core.context import CriteriaContext, MessageEntry
from pydantic import BaseModel

class LexicalRichnessData(BaseModel):
    data: dict[str, float] 

def get_lexical_metrics(criteria_context: CriteriaContext, message_entry: MessageEntry) -> LexicalRichnessData:
    if not message_entry.parts_and_lemmas.lemmas:
        return {"ttr": 0.0, "mattr": 0.0, "mtld": 0.0, "hdd": 0.0}

    lex = LexicalRichness(message_entry.parts_and_lemmas.lemmas, preprocessor=None, tokenizer=None)

    ttr = lex.ttr

    window_size = 25 if len(message_entry.parts_and_lemmas.lemmas) >= 25 else len(message_entry.parts_and_lemmas.lemmas)
    mattr = lex.mattr(window_size=window_size)

    try:
        mtld = lex.mtld(threshold=0.72)
    except Exception:
        mtld = 0.0

    try:
        draws = 42 if len(message_entry.parts_and_lemmas.lemmas) >= 42 else len(message_entry.parts_and_lemmas.lemmas)
        hdd = lex.hdd(draws=draws)
    except Exception:
        hdd = 0.0

    return LexicalRichnessData(data={
        "ttr": ttr,
        "mattr": mattr,
        "mtld": mtld,
        "hdd": hdd
    })