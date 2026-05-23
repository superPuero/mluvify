from fastapi import HTTPException, Depends
from typing import Annotated
import spacy
from pydantic import BaseModel

class SpacyTokenizeResult(BaseModel):
    lemmas: list[str]
    parts: list[str]

class SpacyModel:
    def __init__(self, model_name: str) -> None:
        self.model = spacy.load(model_name)
        
    def tokenize(self, text: str) -> SpacyTokenizeResult:
        doc = self.model(text);
        lemmas: list[str];
        parts: list[str];
        
        for token in doc:
            if token.is_punct:
                parts.append(token.text)
            elif token.is_space:
                continue
            else:
                lemmas.append(token.lemma_)
                parts.append(token.pos_)
                
        return SpacyTokenizeResult(lemmas=lemmas, parts=parts);

    
spacy_model: SpacyModel = SpacyModel("cs_core_news_sm")
SpacyModelDep = Annotated[SpacyModel, Depends(spacy_model)]


