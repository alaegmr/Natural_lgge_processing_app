import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

def plot_and_save_character_heatmap(json_path, output_image_path, show_zeros=False, threshold=0.001):
    """Affiche et sauvegarde une heatmap des cooccurrences de caractères arabes avec intensité selon la probabilité."""
    print("🔄 Chargement :", json_path)

    # Charger les données
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    char_order = data['metadata']['character_order']
    matrix_data = data['matrix']['data']
    print(f"✅ {len(char_order)} caractères chargés")

    # Construire la matrice carrée
    size = len(char_order)
    matrix = np.zeros((size, size))
    char_index = {char: idx for idx, char in enumerate(char_order)}

    for row in matrix_data:
        i = char_index[row['from']]
        for col in row['correlations']:
            j = char_index[col['to']]
            matrix[i, j] = col['value']

    # Appliquer un seuil
    matrix[matrix < threshold] = 0

    # Masque des zéros si show_zeros = False
    mask = (matrix == 0) if not show_zeros else None

    # Créer la figure avec taille proportionnelle à la matrice
    fig, ax = plt.subplots(figsize=(size * 0.5, size * 0.5))  # Ajustez le facteur pour agrandir/réduire les carreaux

    # Palette bleu clair à bleu foncé
    cmap = sns.light_palette("blue", as_cmap=True)

    # Affichage de la heatmap
    sns.heatmap(matrix, xticklabels=char_order, yticklabels=char_order,
                cmap=cmap, mask=mask, linewidths=0.5, square=True,
                cbar_kws={'label': 'Probabilité'}, ax=ax)

    # Inverser Y pour origine en bas à gauche
    ax.invert_yaxis()

    # Titre et labels
    plt.title("Heatmap des Cooccurrences de Caractères Arabes", fontsize=18, pad=20)
    plt.xlabel("Caractère suivant", fontsize=14)
    plt.ylabel("Caractère précédent", fontsize=14)
    plt.xticks(rotation=90, fontsize=10)
    plt.yticks(rotation=0, fontsize=10)

    # Étirer les carreaux sur toute la figure
    plt.tight_layout()

    # Sauvegarde de l'image
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
    print(f"💾 Image sauvegardée dans : {output_image_path}")

    # Affichage
    plt.show()

# 🔧 Appel de la fonction
json_path = '../../data/processed/char_matrix_probabilities.json'
image_path = '../../data/processed/char_heatmap.png'
plot_and_save_character_heatmap(json_path, image_path, show_zeros=False)
