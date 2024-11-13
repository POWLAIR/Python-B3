import os
import numpy as np
from collections import Counter, defaultdict


# ------------------POST-TRAITEMENT------------------

# Fonction pour lire le fichier de logs
def read_log():
    filepath = os.path.join(os.path.dirname(__file__), "data_nasa_log.txt")
    with open(filepath) as file:
        logs = file.readlines()
    return logs

# Charger les logs
logs = read_log()

# Liste des noms à rechercher
personnel_habilite = ["erikson", "mike", "helen", "jack", "phil", "meryll", "katarina", "sylvia"]

# ---------------------CRACK SEG 1----------------------

# Fonction pour vérifier si une ligne contient un prénom mélangé avec des lettres en trop
def find_scrambled_name_in_line(line, names):
    line_counter = Counter(line)
    for name in names:
        name_counter = Counter(name)
        # Vérifie si chaque lettre du prénom apparaît au moins autant de fois dans la ligne
        if all(line_counter[char] >= count for char, count in name_counter.items()):
            return name
    return None



# ---------------------CRACK SEG 2 & 3----------------------

# Conversion du binaire en entier
def binaire_vers_decimal(binaire):
    try:
        decimal = int(binaire, 2)
        return decimal
    except ValueError:
        return "Entrée invalide. Assurez-vous d'entrer une chaîne de caractères binaire (composée de 0 et 1 uniquement)."

    
    

# ----------------RECUPERATIONS DES LOGS----------------
# Dictionnaire pour stocker les logs traitées
logs_decrypted = {}
modifications_summary = defaultdict(lambda: {"count": 0, "lines_modified": 0})

for log in logs:
    if "monitoring.py" in log: 
        segments = log.split("-")  # Découpage du log
        if  segments[1].endswith("$$$$"):
        
            # Décripter les noms
            segment_nom = find_scrambled_name_in_line(segments[0], personnel_habilite)
            
            # Décryptage du segment binaire
            segment_decimal = binaire_vers_decimal(segments[9])
            
        
        
            # Construire la version décryptée du log
            decrypted_log = log
            if segment_decimal and segment_nom is not None:
                decrypted_log = f"{segment_nom}-{segments[1]}-{segments[2]}-{segments[3]}-{segments[4]}-{segment_decimal}"
        
            # Ajouter la log originale et décryptée au dictionnaire
            logs_decrypted[log.strip()] = decrypted_log.strip()
            
            # Enregistrer la modification par utilisateur avec le numéro de ligne
            modifications_summary[segment_nom]["count"] += 1
            modifications_summary[segment_nom]["lines_modified"] += segment_decimal
            
            
# Afficher les logs décryptées
print("---------------------------- Logs Décryptées ----------------------------")
for original, decrypted in logs_decrypted.items():
    print("Log décryptée :", decrypted)

# Afficher le tableau des modifications par personne
print("\n------------------------ Tableau des Modifications -----------------------")
print(f"{'Nom':<15} {'Nombre de modifications':<25} {'Total des lignes modifiées'}")
print("-" * 70)
for name, summary in modifications_summary.items():
    print(f"{name:<15} {summary['count']:<25} {summary['lines_modified']}")