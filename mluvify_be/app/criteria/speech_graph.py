import networkx as nx
import numpy as np
from app.core.context import CriteriaContext, MessageEntry
from networkx import DiGraph

def speech_graph_criteria(criteria_context: CriteriaContext, graph_model: DiGraph, message_entry: MessageEntry) -> int:
    if len(message_entry.parts_and_lemmas.lemmas) < 2:
        return -4
    else:
        G = nx.DiGraph()

        for i in range(len(message_entry.parts_and_lemmas.lemmas) - 1):
            word_from = message_entry.parts_and_lemmas.lemmas[i]
            word_to = message_entry.parts_and_lemmas.lemmas[i+1]
            G.add_edge(word_from, word_to)

        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()

        density = nx.density(G)

        clustering_coeff = nx.average_clustering(G.to_undirected())

        scc = nx.number_strongly_connected_components(G)

        l1_loops = 0
        for i in range(len(message_entry.parts_and_lemmas.lemmas) - 1):
            if message_entry.parts_and_lemmas.lemmas[i] == message_entry.parts_and_lemmas.lemmas[i+1]:
                l1_loops += 1

        l2_loops = 0
        for i in range(len(message_entry.parts_and_lemmas.lemmas) - 2):
            if message_entry.parts_and_lemmas.lemmas[i] == message_entry.parts_and_lemmas.lemmas[i+2] and message_entry.parts_and_lemmas.lemmas[i] != message_entry.parts_and_lemmas.lemmas[i+1]:
                l2_loops += 1

        print(f"Nodes: {num_nodes}")
        print(f"Edges: {num_edges}")
        print(f"Density of graph: {density:.3f}")
        print(f"Coefficient cluster: {clustering_coeff:.3f}")
        print(f"Repeating words (L1 loops): {l1_loops}")
        print(f"Loops (L2 loops): {l2_loops}")

        if clustering_coeff > 0.3 or l2_loops > 2:
            print("Here is loops")
            return +12
            # print("You have some alzheimer")
        else:
            return -12
            # print("Everything is ok.")