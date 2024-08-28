import os
import csv
import json
from collections import defaultdict

# Charger les associations identifiant -> fichier Java
with open('mutants_files.json', 'r') as f:
    mutant_to_file = json.load(f)

# Dictionnaire pour stocker les résultats
results = defaultdict(lambda: defaultdict(int))

# Parcourir tous les fichiers csv dans le répertoire courant
for filename in os.listdir('.'):
    if filename.endswith('.csv'):
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Ignorer l'en-tête
            for row in reader:
                if len(row) == 2:
                    mutant_no = int(row[0])
                    status = row[1]
                    
                    # Regrouper FAIL, UNCOV, TIME sous KILLED
                    if status in ["FAIL", "EXC", "TIME"]:
                        results[mutant_no]["KILLED"] += 1
                    else:
                        results[mutant_no][status] += 1

# Enrichir les résultats avec le nom du fichier Java associé
gamecontrollerjson = {}
gridjson = {}
tilejson = {}

for mutant_no, status_counts in results.items():
    java_file = mutant_to_file.get(str(mutant_no), "Unknown")
    if java_file != "Unknown":
        entry = {
            "file": java_file,
            "statuses": dict(status_counts)
        }
        if java_file == "GameController":
            gamecontrollerjson[mutant_no] = entry
        elif java_file == "Grid":
            gridjson[mutant_no] = entry
        elif java_file == "Tile":
            tilejson[mutant_no] = entry

# Créer les répertoires si nécessaire et sauvegarder les résultats dans des fichiers JSON
os.makedirs('./GameController', exist_ok=True)
with open('./GameController/resultats.json', 'w') as jsonfile:
    json.dump(gamecontrollerjson, jsonfile, indent=4)

os.makedirs('./Grid', exist_ok=True)
with open('./Grid/resultats.json', 'w') as jsonfile:
    json.dump(gridjson, jsonfile, indent=4)

os.makedirs('./Tile', exist_ok=True)
with open('./Tile/resultats.json', 'w') as jsonfile:
    json.dump(tilejson, jsonfile, indent=4)

print("Les fichiers 'resultats.json' ont été créés avec succès dans les dossiers respectifs.")
