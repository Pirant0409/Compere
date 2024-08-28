import os
import json

# Chemin du dossier principal "mutants"
mutants_dir = './mutants'

# Dictionnaire pour stocker les associations identifiant -> fichier .java
mutants_files = {}

# Parcourir chaque sous-dossier dans "mutants"
for root, dirs, files in os.walk(mutants_dir):
    for file in files:

        if file.endswith('.java'):
            #Récupérer le chemin complet du fichier et prendre le nom du deuxieme dossier
            identifiant = root.split('\\')[1]
            
            # Récupérer le nom du fichier sans l'extension .java
            file_name = os.path.splitext(file)[0]
            
            # Ajouter au dictionnaire
            mutants_files[identifiant] = file_name

# Sauvegarder le dictionnaire dans un fichier JSON
with open('mutants_files.json', 'w') as jsonfile:
    json.dump(mutants_files, jsonfile, indent=4)

print("Le fichier 'mutants_files.json' a été créé avec succès.")
