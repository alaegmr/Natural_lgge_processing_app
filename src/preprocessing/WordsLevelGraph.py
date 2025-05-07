import json
import networkx as nx
import matplotlib.pyplot as plt


def load_word_matrix(file_path):
    """Charge la matrice de transition de mots depuis un fichier JSON"""
    print("🔄 Chargement de la matrice de transition...")
    with open(file_path, 'r', encoding='utf-8') as f:
        word_matrix = json.load(f)  # Charge directement la liste
    print(f"✅ {len(word_matrix)} lignes de données chargées avec succès.")
    return word_matrix


def build_word_graph(word_matrix):
    """Construit un graphe de transitions de mots avec probabilités"""
    print("🔄 Construction du graphe des mots...")
    G = nx.DiGraph()  # Graphe orienté pour les transitions

    for entry in word_matrix:
        word = entry["word"]
        print(f"Traitement du mot: {word}")
        for transition in entry["transitions"]:
            next_word = transition["word"]
            probability = transition["probability"]
            # Ajouter les noeuds (si ce n'est pas déjà fait)
            G.add_node(word)
            G.add_node(next_word)
            # Ajouter l'arc avec la probabilité comme poids
            G.add_edge(word, next_word, weight=probability)

    print(f"✅ {len(G.nodes)} noeuds et {len(G.edges)} arcs ajoutés au graphe.")
    return G


def draw_word_graph(G):
    """Dessine et affiche le graphe des transitions de mots"""
    print("🔄 Dessin du graphe...")
    plt.figure(figsize=(12, 12))

    # Poser les noeuds pour une meilleure disposition
    pos = nx.spring_layout(G, seed=42)  # Disposition automatique (spring layout)

    # Dessiner les noeuds
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color="lightblue", alpha=0.7)

    # Dessiner les arêtes avec les probabilités comme labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.7, edge_color="gray")

    # Afficher les labels des noeuds (mots)
    nx.draw_networkx_labels(G, pos, font_size=12, font_color="black")

    # Afficher les labels des arêtes (probabilités)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    plt.title("Graphe des transitions de mots avec probabilités")
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    # Chemin vers le fichier de matrice de mots
    word_matrix_path = "../../data/processed/word_matrix.json"

    # Charger la matrice de transition des mots
    try:
        word_matrix = load_word_matrix(word_matrix_path)
    except Exception as e:
        print(f"Erreur lors du chargement du fichier : {e}")
        exit()

    # Vérification de la structure de la donnée
    print(f"✅ Vérification des données : {word_matrix[:5]}... (Affichage des 5 premières entrées)")

    # Construire le graphe des transitions de mots
    try:
        G = build_word_graph(word_matrix)
    except Exception as e:
        print(f"Erreur lors de la construction du graphe : {e}")
        exit()

    # Dessiner et afficher le graphe
    try:
        draw_word_graph(G)
    except Exception as e:
        print(f"Erreur lors du dessin du graphe : {e}")
        exit()

    print("✅ Graphe des transitions de mots affiché avec succès.")
