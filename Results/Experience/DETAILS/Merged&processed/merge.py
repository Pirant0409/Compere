import os
import json
from collections import defaultdict

# Dictionnaire pour stocker les résultats fusionnés
merged_results = {
    "GameController": defaultdict(lambda: {"file": "GameController", "statuses": defaultdict(dict)}),
    "Grid": defaultdict(lambda: {"file": "Grid", "statuses": defaultdict(dict)}),
    "Tile": defaultdict(lambda: {"file": "Tile", "statuses": defaultdict(dict)})
}

# Parcourir tous les répertoires S1, GrpA, GrpB
for root, dirs, files in os.walk('.'):
    for file in files:
        if file == "resultats.json":
            # Déterminer le chemin du fichier
            filepath = os.path.join(root, file)
            
            # Déterminer la source à partir du nom du dossier parent (S1, GrpA, GrpB)
            source = os.path.basename(os.path.dirname(os.path.dirname(filepath)))
            if source in ['Grid', 'Tile', 'GameController']:
                source = os.path.basename(os.path.dirname(filepath))

            # Charger le fichier JSON
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Déterminer dans quel type de dossier on se trouve (Grid, Tile, GameController)
            for mutant_no, mutant_data in data.items():
                file_type = mutant_data["file"]  # Devrait être Grid, Tile, ou GameController
                
                # Fusionner les données
                for status, count in mutant_data["statuses"].items():
                    if status in merged_results[file_type][mutant_no]["statuses"][source]:
                        merged_results[file_type][mutant_no]["statuses"][source][status] += count
                    else:
                        merged_results[file_type][mutant_no]["statuses"][source][status] = count

# Sauvegarder les résultats fusionnés dans des fichiers JSON
for file_type, results in merged_results.items():
    output_file = f'resultats_{file_type.lower()}.json'
    with open(output_file, 'w') as jsonfile:
        json.dump(results, jsonfile, indent=4)

print("Les fichiers fusionnés ont été créés avec succès.")
