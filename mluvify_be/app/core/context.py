from typing import Annotated
from fastapi import Depends

class MessageEntry:
    def __init__(self) -> None:
        self.text: str = "";

class CriteriaContext:
    def __init__(self) -> None:
        self.criterias: dict[str, list[float]] = {}
        self.message: list[(str, )] = {}    

criteria_context: CriteriaContext = CriteriaContext();

CriteriaContextDep = Annotated[CriteriaContext, Depends(criteria_context)]