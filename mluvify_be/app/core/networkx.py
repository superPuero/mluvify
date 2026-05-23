from networkx import DiGraph
from typing import Annotated
from fastapi import Depends

networkx_graph: DiGraph = DiGraph()

NetworkxDep = Annotated[DiGraph, Depends(networkx_graph)]