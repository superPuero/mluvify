import networkx as nx
import numpy as np
from app.core.context import CriteriaContext, MessageEntry
from app.core.networkx import NetxGraph
from pydantic import BaseModel

class SpeechGraphData(BaseModel):
    data: dict[str, float]

def speech_graph_criteria(criteria_context: CriteriaContext, graph_model: NetxGraph, message_entry: MessageEntry) -> SpeechGraphData:
    for i in range(len(message_entry.parts_and_lemmas.lemmas) - 1):
        word_from = message_entry.parts_and_lemmas.lemmas[i]
        word_to = message_entry.parts_and_lemmas.lemmas[i+1]
        graph_model.graph.add_edge(word_from, word_to)

    num_nodes: float = graph_model.graph.number_of_nodes()
    num_edges: float = graph_model.graph.number_of_edges()

    density: float = nx.density(graph_model.graph)

    clustering_coeff: float = nx.average_clustering(graph_model.graph.to_undirected())

    scc = nx.number_strongly_connected_components(graph_model.graph)

    l1_loops: float = 0
    for i in range(len(message_entry.parts_and_lemmas.lemmas) - 1):
        if message_entry.parts_and_lemmas.lemmas[i] == message_entry.parts_and_lemmas.lemmas[i+1]:
            l1_loops += 1

    l2_loops: float = 0
    for i in range(len(message_entry.parts_and_lemmas.lemmas) - 2):
        if message_entry.parts_and_lemmas.lemmas[i] == message_entry.parts_and_lemmas.lemmas[i+2] and message_entry.parts_and_lemmas.lemmas[i] != message_entry.parts_and_lemmas.lemmas[i+1]:
            l2_loops += 1
    return SpeechGraphData(data={
        "nodes": num_nodes,
        "edges": num_edges,
        "density": density,
        "clustering_coeff": clustering_coeff,
        "l1_loops": l1_loops,
        "l2_loops": l2_loops
    })