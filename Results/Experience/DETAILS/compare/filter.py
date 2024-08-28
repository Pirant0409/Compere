import json

# Chargement des fichiers JSON fusionnés
def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Sauvegarde des fichiers JSON filtrés
def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Filtrer les données selon les critères spécifiés
def filter_data(data):
    filtered_data = {}
    for mutant_no, mutant_data in data.items():
        statuses = mutant_data['statuses']
        grpA_statuses = statuses.get('GrpA', {})
        grpB_statuses = statuses.get('GrpB', {})
        
        # Vérifier les conditions de filtrage
        grpA_has_uncov_only = (set(grpA_statuses.keys()) == {'UNCOV','LIVE'})
        grpB_has_killed = ('KILLED' in grpB_statuses)
        
        grpB_has_uncov_only = (set(grpB_statuses.keys()) == {'UNCOV','LIVE'})
        grpA_has_killed = ('KILLED' in grpA_statuses)
        
        if (grpA_has_uncov_only and grpB_has_killed) or (grpB_has_uncov_only and grpA_has_killed):
            filtered_data[mutant_no] = mutant_data
    
    return filtered_data

# Liste des fichiers JSON à traiter
files = {
    'resultats_gamecontroller.json': 'resultats_filtered_gamecontroller_best.json',
    'resultats_grid.json': 'resultats_filtered_grid_best.json',
    'resultats_tile.json': 'resultats_filtered_tile_best.json'
}

# Traitement de chaque fichier
for input_file, output_file in files.items():
    data = load_json(input_file)
    filtered_data = filter_data(data)
    save_json(filtered_data, output_file)
    print(f"Les résultats filtrés ont été sauvegardés dans '{output_file}'.")

print("Tous les fichiers ont été traités.")
