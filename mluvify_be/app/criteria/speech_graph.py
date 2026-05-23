# import networkx as nx
# import numpy as np
# from lemmas_part import lemmas_from_text

# def speech_graph_criteria() -> int:
#     if len(lemmas_from_text) < 2:
#         print("Not enough words.")
#     else:
#         G = nx.DiGraph()

#         for i in range(len(lemmas_from_text) - 1):
#             word_from = lemmas_from_text[i]
#             word_to = lemmas_from_text[i+1]
#             G.add_edge(word_from, word_to)

#         num_nodes = G.number_of_nodes()
#         num_edges = G.number_of_edges()

#         density = nx.density(G)

#         clustering_coeff = nx.average_clustering(G.to_undirected())

#         scc = nx.number_strongly_connected_components(G)

#         l1_loops = 0
#         for i in range(len(lemmas_from_text) - 1):
#             if lemmas_from_text[i] == lemmas_from_text[i+1]:
#                 l1_loops += 1

#         l2_loops = 0
#         for i in range(len(lemmas_from_text) - 2):
#             if lemmas_from_text[i] == lemmas_from_text[i+2] and lemmas_from_text[i] != lemmas_from_text[i+1]:
#                 l2_loops += 1

#         print(f"Nodes: {num_nodes}")
#         print(f"Edges: {num_edges}")
#         print(f"Density of graph: {density:.3f}")
#         print(f"Coefficient cluster: {clustering_coeff:.3f}")
#         print(f"Repeating words (L1 loops): {l1_loops}")
#         print(f"Loops (L2 loops): {l2_loops}")

#         if clustering_coeff > 0.3 or l2_loops > 2:
#             print("Here is loops")
#             return +12
#             # print("You have some alzheimer")
#         else:
#             return -12
#             # print("Everything is ok.")