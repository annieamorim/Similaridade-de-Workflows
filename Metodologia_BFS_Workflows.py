from google.colab import drive
drive.mount('/content/drive')

import os
import json
import networkx as nx
import matplotlib.pyplot as plt
import time
import psutil
from networkx.drawing.nx_pydot import graphviz_layout

input_directory = "Workflows com Pesos/"

workflows = []
filenames = []
for filename in os.listdir(input_directory):
    if filename.endswith('.graphml'):
        filepath = os.path.join(input_directory, filename)
        G = nx.read_graphml(filepath)
        workflows.append(G)
        filenames.append(filename.replace('.graphml', '.json'))

input_directory = "Workflows com Pesos/"

workflows = []
filenames = []

for filename in os.listdir(input_directory):
    if filename.endswith('.graphml'):
        filepath = os.path.join(input_directory, filename)
        G = nx.read_graphml(filepath)
        workflows.append(G)
        filenames.append(filename.replace('.graphml', ''))

for i, G in enumerate(workflows):
    plt.figure(figsize=(12, 12))
    plt.title(filenames[i])

    pos = graphviz_layout(G, prog='dot')

    node_weights = nx.get_node_attributes(G, 'weight')
    nodes = nx.draw_networkx_nodes(G, pos, node_size=700, node_color=list(node_weights.values()), cmap=plt.cm.viridis)
    edges = nx.draw_networkx_edges(G, pos)

    nx.draw_networkx_labels(G, pos)
    plt.colorbar(nodes)
    plt.axis('on')
    plt.show()

filename_to_index = {filename: i+1 for i, filename in enumerate(filenames)}
specific_filename = 'workflow_611'
print(f"Index for {specific_filename}: {filename_to_index[specific_filename]}")


def bfs_order_using_nx(graph):
    visited = set()
    order = []

    for node in graph.nodes():
        if node not in visited:
            bfs_tree = nx.bfs_tree(graph, node)
            for bfs_node in bfs_tree.nodes():
                visited.add(bfs_node)
                order.append(graph.nodes[bfs_node]['label'])

    return order

def bfs_order_using_nx(graph):
    visited = set()
    order = []

    for node in graph.nodes():
        if node not in visited:
            bfs_tree = nx.bfs_tree(graph, node)
            for bfs_node in bfs_tree.nodes():
                visited.add(bfs_node)
                order.append(graph.nodes[bfs_node]['label'])

    return order

def calculate_similarity(ref_graph, other_graph, ref_order):
    other_order = bfs_order_using_nx(other_graph)
    common_labels = set(ref_order) & set(other_order)
    common_nodes = [node for node, data in ref_graph.nodes(data=True) if data['label'] in common_labels]
    return sum(ref_graph.nodes[node]['weight'] for node in common_nodes)

def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for index2, char2 in enumerate(s2):
        new_distances = [index2 + 1]
        for index1, char1 in enumerate(s1):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(1 + min((distances[index1], distances[index1 + 1], new_distances[-1])))
        distances = new_distances

    return distances[-1]

def memory_usage_psutil():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss / 1024

start_time = time.time()
memory_before = memory_usage_psutil()

ref_index = filename_to_index[specific_filename] - 1
ref_workflow = workflows[ref_index]
ref_order = bfs_order_using_nx(ref_workflow)

similarities = {}
for i, workflow in enumerate(workflows):
    if i != ref_index:
        order = bfs_order_using_nx(workflow)
        sim = calculate_similarity(ref_workflow, workflow, ref_order)
        similarities[i] = sim

similar_workflows = [i for i, sim in similarities.items() if sim >= 0.5]

lev_distances = {}
for i in similar_workflows:
    workflow = workflows[i]
    order = bfs_order_using_nx(workflow)
    dist = levenshtein_distance(ref_order, order)
    lev_distances[i] = dist

most_similar_workflow = min(lev_distances, key=lev_distances.get)

end_time = time.time()
memory_after = memory_usage_psutil()

print(f"The most similar Workflow to Workflow {ref_index + 1} based on Levenshtein distance is Workflow {most_similar_workflow + 1} with a distance of {lev_distances[most_similar_workflow]}.")
print(f"Node sequence of Workflow {ref_index + 1} ({filenames[ref_index]}): {ref_order}")
print(f"Node sequence of Workflow {most_similar_workflow + 1} ({filenames[most_similar_workflow]}): {bfs_order_using_nx(workflows[most_similar_workflow])}")

execution_time = end_time - start_time
print(f"Tempo de execução: {execution_time} segundos")

memory_used = memory_after - memory_before
print(f"Memória utilizada: {memory_used} KB")
