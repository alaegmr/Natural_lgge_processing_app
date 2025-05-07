import json
import networkx as nx
import matplotlib.pyplot as plt
import os

def build_graph_from_character_matrix(json_path, min_weight=0.001, save_path=None):
    """Construit, visualise et enregistre un graphe clair et moderne à partir de la matrice de cooccurrence des caractères"""

    # Charger les données
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    char_order = data['metadata']['character_order']
    matrix_data = data['matrix']['data']

    G = nx.DiGraph()

    # Ajouter les nœuds et les arêtes filtrées
    for row in matrix_data:
        from_char = row['from']
        G.add_node(from_char)
        for correlation in row['correlations']:
            to_char = correlation['to']
            weight = correlation['value']
            if weight >= min_weight:
                G.add_edge(from_char, to_char, weight=round(weight, 4))

    # Disposition
    pos = nx.spring_layout(G, seed=42, k=2, scale=2)  # 🔥 Agrandir avec scale=2

    # Taille dynamique
    fig = plt.figure(figsize=(max(20, len(G.nodes()) * 0.8), 20))  # 🔥 Encore plus grand

    # Style moderne
    node_colors = '#00b4d8'  # Bleu océan
    edge_colors = '#adb5bd'  # Gris doux

    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color=node_colors, edgecolors='white', linewidths=2)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrowsize=20, alpha=0.7, width=2)
    nx.draw_networkx_labels(G, pos, font_size=18, font_weight='bold', font_color='white')

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color='#6c757d')

    plt.title('Graphique des Cooccurrences de Caractères Arabes', fontsize=24, fontweight='bold', color='#0077b6', pad=30)
    plt.axis('off')

    # 🔥 Supprimer tight_layout qui serre l'image
    # 🔥 Ajouter plt.margins pour laisser respirer
    plt.margins(0.2)  # 20% d'espace autour

    # Sauvegarder
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[✓] Graphe enregistré sous : {save_path}")

    plt.show()

# Utilisation
json_path = '../../data/processed/char_matrix_probabilities.json'

# Construire un chemin vers processed pour sauvegarder
current_dir = os.path.dirname(__file__)
save_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'data', 'processed', 'char_graph.png'))

build_graph_from_character_matrix(json_path, min_weight=0.002, save_path=save_path)
