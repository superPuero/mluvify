from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel
from app.core.spacy import SpacyPartsAndLemmas, SpacyModel
from app.core.whisper import WhisperServiceManager, WhisperModel

class MessageEntry(BaseModel):
    text: str
    sentences: list[str]       
    parts_and_lemmas: SpacyPartsAndLemmas  

class CriteriaContextData(BaseModel):
    criterias: dict[str, list[float]]
    all_messages: list[str]
                                                                                                           
class CriteriaContext:
    def __init__(self) -> None:
        self.llm_msg = []        
        self.criteria_data = CriteriaContextData(
            criterias={},
            all_messages=[]
        )
    def __call__(self):
        return self
                                    
criteria_context: CriteriaContext = CriteriaContext();

CriteriaContextDep = Annotated[CriteriaContext, Depends(criteria_context)]