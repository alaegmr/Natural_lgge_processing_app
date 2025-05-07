import json
from collections import Counter
import matplotlib.pyplot as plt
import os

# Construire le chemin du fichier
current_dir = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'data', 'processed', 'finalDictionary.json'))

# Charger le fichier JSON
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Compter les occurrences de chaque méthode
methods = [item['method'] for item in data]
counter = Counter(methods)

# Calculer les pourcentages
total = sum(counter.values())
percentages = {method: (count / total) * 100 for method, count in counter.items()}

# Afficher les résultats
for method, percentage in percentages.items():
    print(f"{method}: {percentage:.2f}%")

# Tracer un camembert
labels = list(percentages.keys())
sizes = list(percentages.values())

plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#66b3ff', '#ff9999', '#99ff99', '#ffcc99'])
plt.axis('equal')
plt.title('Répartition des méthodes de recherche')
plt.show()
