# Python B3 Project

## Description

Ce projet est un ensemble de scripts Python réalisés dans le cadre de votre cursus B3. Il comprend plusieurs modules pour différentes tâches, allant de la manipulation de bases de données à des mini-jeux en console. Voici une brève description des principaux fichiers et dossiers.

## Structure du Projet

### Dossiers et Fichiers Principaux

- **data insup/** : Contient des scripts et des fichiers de traitement de données.

  - **index.py** : Script principal pour le traitement de fichiers JSON volumineux. Il extrait des données de playlists, morceaux et leurs relations, puis les stocke dans une base de données MySQL.
  - **temp_csv/**, **unzipped/** : Dossiers utilisés pour stocker les fichiers temporaires et les données JSON extraites.
  - **venv/** : Environnement virtuel Python pour gérer les dépendances du projet.

- **fusée/** : Module contenant des scripts pour analyser et déchiffrer des logs.

  - **crackPaul.py** : Script qui traite des fichiers de logs, déchiffre des noms mélangés et convertit des segments binaires en décimaux pour des analyses de données.
  - **main.py** : Script qui imprime des coordonnées et leur fiabilité.

- **jeuDonjon/** : Contient un mini-jeu en console.

  - **programmePaul.py** : Jeu de donjon où le joueur explore un donjon en se déplaçant, rencontre des ennemis, et cherche à trouver un trophée pour gagner. Le joueur commence avec 10 points de vie, et le jeu se termine lorsque les victoires nécessaires sont atteintes ou si le joueur perd tous ses points de vie.

- **process_log.log** : Fichier de log des processus.
- **data_nasa_log.txt** : Fichier de log avec les données de la NASA à analyser.
- **README.md** : Ce fichier, expliquant la structure et le but de chaque module.

## Utilisation

### Prérequis

- Python 3.12 ou supérieur.
- [MySQL](https://www.mysql.com/) pour la gestion des bases de données.
- Modules Python nécessaires (voir `requirements.txt` si disponible).

### Exécution

1. **Configuration de la base de données**

   - Assurez-vous que MySQL est installé et configuré.
   - Modifiez les paramètres de connexion dans `index.py` pour correspondre à votre configuration MySQL.

2. **Lancement du traitement de données**

   - Exécutez `index.py` pour commencer le traitement des fichiers JSON et les insérer dans la base de données.

   ```bash
   python data\ insup/index.py
   ```

3. **Déchiffrement des logs**

   - Utilisez `crackPaul.py` pour analyser et déchiffrer les logs de `data_nasa_log.txt`.

   ```bash
   python fusée/crackPaul.py
   ```

4. **Jeu de donjon**

   - Lancer le jeu de donjon avec `programmePaul.py`.

   ```bash
   python jeuDonjon/programmePaul.py
   ```

## Fonctionnalités

### `data insup/index.py`

- Connexion à une base de données MySQL.
- Création de tables pour stocker les playlists, les morceaux et leurs relations.
- Traitement par lots pour gérer de grands fichiers JSON sans surcharger la RAM.
- Optimisation de la taille des batchs en fonction de la vitesse de traitement.

### `fusée/crackPaul.py`

- Lecture et déchiffrement des logs de la NASA.
- Identification de noms mélangés et conversion de segments binaires en décimaux.
- Analyse et affichage des modifications pour chaque utilisateur dans les logs.

### `jeuDonjon/programmePaul.py`

- Jeu de donjon en console où le joueur explore et affronte des ennemis.
- Gestion des déplacements et des rencontres aléatoires avec des ennemis.
- Système de points de vie et de conditions de victoire.

## Auteur

- **Paul Claverie** - Développeur Python B3
- **Bastien Roupert** - Développeur Python B3
