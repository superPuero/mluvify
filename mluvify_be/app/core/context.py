from typing import Annotated
from fastapi import Depends


class CriteriaContext:
    def __init__(self) -> None:
        self.criterias: dict[str, list[float]] = {}


# CriteriaContextDep = Annotated[CriteriaContext, Depends()]