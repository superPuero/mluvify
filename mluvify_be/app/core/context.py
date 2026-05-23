from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel
from app.core.spacy import SpacyPartsAndLemmas, SpacyModel
from app.core.whisper import WhisperServiceManager, WhisperModel

class MessageEntry(BaseModel):
    text: str
    sentences: list[str]       
    parts_and_lemmas: SpacyPartsAndLemmas  
                    
class CriteriaContext:
    def __init__(self) -> None:
        self.criterias: dict[str, list[float]] = {}
        self.all_messages: list[str] = {}            
                                
criteria_context: CriteriaContext = CriteriaContext();

CriteriaContextDep = Annotated[CriteriaContext, Depends(criteria_context)]