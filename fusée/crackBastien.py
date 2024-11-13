import os
from collections import Counter

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

# Fonction pour vérifier si une ligne contient un prénom mélangé avec des lettres en trop
def find_scrambled_name_in_line(line, names_set):
    line_counter = Counter(line)
    for name in names_set:
        name_counter = Counter(name)
        if all(line_counter[char] >= count for char, count in name_counter.items()):
            return name
    return None

# Conversion du binaire en entier
def binaire_vers_decimal(binaire):
    try:
        return int(binaire, 2)
    except ValueError:
        return None

# Pré-traitement pour la recherche rapide des noms
personnel_habilite_set = set(personnel_habilite)

# Dictionnaire pour stocker les logs décryptées par personne et le total des segments décimaux
logs_par_personne = {name: {"logs": [], "total_decimal": 0} for name in personnel_habilite}

# Traitement des logs et regroupement par nom
for log in logs:
    if "monitoring.py" in log: 
        segments = log.split("-")
        
        if len(segments) > 5 and segments[1].endswith('$'):
            segment_nom = find_scrambled_name_in_line(segments[0], personnel_habilite_set)
            segment_decimal = binaire_vers_decimal(segments[9]) if len(segments) > 9 else None
            
            if segment_nom and segment_decimal is not None:
                decrypted_log = f"{segment_nom}-{segments[1]}-{segments[2]}-{segments[3]}-{segments[4]}-{segment_decimal}"
                
                # Ajouter la log décryptée au tableau de la personne concernée
                logs_par_personne[segment_nom]["logs"].append(decrypted_log)
                
                # Ajouter la valeur décimale au total pour cette personne
                logs_par_personne[segment_nom]["total_decimal"] += segment_decimal

# Affichage des logs décryptées par personne avec le total
for person, data in logs_par_personne.items():
    if data["logs"]:  # Afficher uniquement les personnes ayant des logs
        print(f"Logs pour {person} :")
        for decrypted_log in data["logs"]:
            print("  ", decrypted_log)
        print(f"Total des valeurs décimales pour {person} : {data['total_decimal']}")
        print("-----")

# Identifier la personne ayant le plus grand total de segments décimaux
person_with_max_decimal = max(logs_par_personne.items(), key=lambda item: item[1]["total_decimal"])

print(f"La personne avec le plus grand total de segments décimaux est {person_with_max_decimal[0]} avec un total de {person_with_max_decimal[1]['total_decimal']}.")
