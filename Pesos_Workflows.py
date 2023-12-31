import os
import json
import networkx as nx
import matplotlib.pyplot as plt
import random

from google.colab import drive
drive.mount('/content/drive')

def build_graph_from_workflow(workflow_path):
    with open(workflow_path, 'r') as f:
        data = json.load(f)

    G = nx.DiGraph()

    for key, value in data['steps'].items():
        G.add_node(key, label=value['name'])

    for key, value in data['steps'].items():
        for _, conn in value['input_connections'].items():
            G.add_edge(str(conn['id']), key)

    return G

def plot_graph(G):
    pos = nx.spring_layout(G)
    labels = {n: G.nodes[n]['label'] for n in G.nodes}

    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=3000, node_color='skyblue', font_size=6, font_weight='bold', edge_color='gray')
    plt.show()

directory = "caminho dos dados"

for filename in os.listdir(directory):
    if filename.endswith('.json'):
        print(f"Workflow {filename}")
        filepath = os.path.join(directory, filename)
        G = build_graph_from_workflow(filepath)
        plot_graph(G)

process_to_number = {}
current_number = 1

def get_process_number(process_name):
    global current_number
    if process_name not in process_to_number:
        process_to_number[process_name] = current_number
        current_number += 1
    return process_to_number[process_name]

def build_graph_with_normalized_weights_from_workflow(workflow_path):
    with open(workflow_path, 'r') as f:
        data = json.load(f)

    G = nx.DiGraph()

    total_nodes = len(data['steps'])
    random_weights = [random.random() for _ in range(total_nodes)]
    total_random_weights = sum(random_weights)

    normalized_weights = [rw / total_random_weights for rw in random_weights]

    for i, (key, value) in enumerate(data['steps'].items()):
        process_num = get_process_number(value['name'])
        G.add_node(key, label=str(process_num), weight=normalized_weights[i])

    for key, value in data['steps'].items():
        for _, conn in value['input_connections'].items():
            G.add_edge(str(conn['id']), key)

    return G

def plot_graph_with_weights(G):
    pos = nx.spring_layout(G)
    labels = {n: f"{G.nodes[n]['label']} ({G.nodes[n]['weight']:.2f})" for n in G.nodes}

    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=3000, node_color='skyblue', font_size=6, font_weight='bold', edge_color='gray')
    plt.show()

directory = "caminho dos dados"

workflows = []
filenames = []
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)
        G = build_graph_with_normalized_weights_from_workflow(filepath)

        filenames.append(filename)
        workflows.append(G)

        total_weight = sum(node_data['weight'] for _, node_data in G.nodes(data=True))
        print(f"Workflow {filename}")
        plot_graph_with_weights(G)
