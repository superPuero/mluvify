from networkx import DiGraph
from typing import Annotated
from fastapi import Depends

class NetxGraph:
    def __init__(self):
        self.graph: DiGraph = DiGraph() 
              
    def __call__(self):
        return self          

networkx_graph: NetxGraph = NetxGraph()

NetworkxDep = Annotated[NetxGraph, Depends(networkx_graph)]