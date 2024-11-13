import os
import time
import gc
import mysql.connector
import orjson
from concurrent.futures import ProcessPoolExecutor


def connect_to_database():
    print("🔌 Connexion à la base de données...")
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='datapythonplaylist',
            allow_local_infile=True,
            charset='utf8mb4',
            use_unicode=True,
            collation='utf8mb4_unicode_ci',
            autocommit=False  # Utiliser les transactions pour les insertions par batch
        )
        print("✅ Connexion à la base de données réussie")
        return connection
    except mysql.connector.Error as err:
        print(f"❌ Erreur de connexion à la base de données: {err}")
        return None


def create_tables(cursor):
    print("🔧 Création des tables...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS playlists (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            collaborative BOOLEAN,
            num_tracks INT,
            num_albums INT,
            num_followers INT,
            INDEX (name(191))
        ) ENGINE=InnoDB ROW_FORMAT=DYNAMIC DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            track_uri VARCHAR(255) PRIMARY KEY,
            track_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            artist_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            album_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            duration_ms INT,
            INDEX (track_uri(191))
        ) ENGINE=InnoDB ROW_FORMAT=DYNAMIC DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS playlist_tracks (
            playlist_id INT,
            track_uri VARCHAR(255),
            PRIMARY KEY (playlist_id, track_uri),
            FOREIGN KEY (playlist_id) REFERENCES playlists(id),
            FOREIGN KEY (track_uri) REFERENCES tracks(track_uri),
            INDEX (track_uri(191))
        ) ENGINE=InnoDB ROW_FORMAT=DYNAMIC DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    ''')
    print("✅ Tables créées avec succès")


def batch_insert_into_database(cursor, playlists_data_batch, tracks_data_batch, playlist_tracks_data_batch):
    try:
        if playlists_data_batch:
            cursor.executemany('''
                INSERT IGNORE INTO playlists (id, name, collaborative, num_tracks, num_albums, num_followers)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', playlists_data_batch)
        
        if tracks_data_batch:
            cursor.executemany('''
                INSERT IGNORE INTO tracks (track_uri, track_name, artist_name, album_name, duration_ms)
                VALUES (%s, %s, %s, %s, %s)
            ''', list(tracks_data_batch))

        if playlist_tracks_data_batch:
            cursor.executemany('''
                INSERT IGNORE INTO playlist_tracks (playlist_id, track_uri)
                VALUES (%s, %s)
            ''', playlist_tracks_data_batch)

        cursor._connection.commit()
        print(f"✅ Batch inséré avec succès: {len(playlists_data_batch)} playlists, "
              f"{len(tracks_data_batch)} tracks, {len(playlist_tracks_data_batch)} relations.")
    except mysql.connector.Error as err:
        print(f"❌ Erreur lors de l'insertion dans la base de données: {err}")
        cursor._connection.rollback()
    finally:
        gc.collect()
        print("♻️ Mémoire nettoyée après l'insertion du batch")


def process_file(file_path, seen_tracks):
    start_time = time.time()
    playlists_data = []
    tracks_data = set()
    playlist_tracks_data = []

    if os.path.getsize(file_path) == 0:
        print(f"⚠️ Fichier vide ignoré: {file_path}")
        return playlists_data, tracks_data, playlist_tracks_data, 0, seen_tracks

    try:
        with open(file_path, 'rb') as json_file:
            data = orjson.loads(json_file.read())
            for playlist in data.get("playlists", []):
                playlist_id = playlist.get('pid')
                playlists_data.append((
                    playlist_id, playlist.get('name'),
                    playlist.get('collaborative') == "true", playlist.get('num_tracks'),
                    playlist.get('num_albums'), playlist.get('num_followers')
                ))

                for track in playlist.get('tracks', []):
                    track_uri = track.get('track_uri')
                    if track_uri not in seen_tracks:
                        tracks_data.add((
                            track_uri, track.get('track_name'),
                            track.get('artist_name'), track.get('album_name'),
                            track.get('duration_ms')
                        ))
                        seen_tracks[track_uri] = True
                    playlist_tracks_data.append((playlist_id, track_uri))

        processing_time = time.time() - start_time
        print(f"✅ Fichier {file_path} traité en {processing_time:.2f} secondes")
        return playlists_data, tracks_data, playlist_tracks_data, processing_time, seen_tracks
    except (orjson.JSONDecodeError, MemoryError) as e:
        processing_time = time.time() - start_time
        print(f"❌ Erreur lors du traitement du fichier {file_path}: {e}")
        return [], set(), [], processing_time, seen_tracks


def sort_files_by_size(json_files):
    return sorted(json_files, key=lambda f: os.path.getsize(f))


def main():
    print("🚀 Début du programme")

    connection = connect_to_database()
    if not connection:
        print("❌ Impossible de se connecter à la base de données. Arrêt du programme.")
        return

    cursor = connection.cursor()
    create_tables(cursor)

    print("🔧 Désactivation des index pour accélérer les insertions")
    cursor.execute("ALTER TABLE playlists DISABLE KEYS")
    cursor.execute("ALTER TABLE tracks DISABLE KEYS")
    cursor.execute("ALTER TABLE playlist_tracks DISABLE KEYS")

    data_folder = "unziped/data"
    json_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith('.json')]
    json_files = sort_files_by_size(json_files)
    print(f"📊 Nombre total de fichiers JSON à traiter : {len(json_files)}")

    initial_batch_size = 5000
    batch_size = initial_batch_size
    playlists_batch = []
    tracks_batch = set()
    playlist_tracks_batch = []

    total_start_time = time.time()
    total_files_processed_time = 0
    seen_tracks = {}

    print("🚧 Début du traitement des fichiers JSON")
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(process_file, file, seen_tracks) for file in json_files]
        
        for i, future in enumerate(futures, 1):
            playlists_data, tracks_data, playlist_tracks_data, file_processing_time, updated_seen_tracks = future.result()
            
            playlists_batch.extend(playlists_data)
            tracks_batch.update(tracks_data)
            playlist_tracks_batch.extend(playlist_tracks_data)
            seen_tracks.update(updated_seen_tracks)

            total_files_processed_time += file_processing_time

            if len(playlists_batch) >= batch_size:
                batch_insert_into_database(cursor, playlists_batch, tracks_batch, playlist_tracks_batch)
                playlists_batch.clear()
                tracks_batch.clear()
                playlist_tracks_batch.clear()

                # Ajustement dynamique de la taille des batchs
                if i % 10 == 0:
                    avg_time_per_file = total_files_processed_time / i
                    if avg_time_per_file < 0.5:  # Si le traitement est rapide, augmenter la taille du batch
                        batch_size = min(batch_size * 2, 20000)
                    elif avg_time_per_file > 2:  # Si le traitement est lent, réduire la taille du batch
                        batch_size = max(batch_size // 2, initial_batch_size)

            # Calcul du nombre de fichiers traités par seconde
            files_per_second = i / (time.time() - total_start_time)

            if i % 10 == 0:
                avg_time_per_file = total_files_processed_time / i
                print(f"📊 Progression : {i}/{len(json_files)} fichiers traités - Temps moyen/fichier: {avg_time_per_file:.2f} secondes - Fichiers par seconde: {files_per_second:.2f} - Taille du batch: {batch_size}")

    # Insertion des données restantes si non vidées
    if playlists_batch:
        print("⬇️ Insertion des données restantes")
        batch_insert_into_database(cursor, playlists_batch, tracks_batch, playlist_tracks_batch)

    print("🔧 Réactivation des index")
    cursor.execute("ALTER TABLE playlists ENABLE KEYS")
    cursor.execute("ALTER TABLE tracks ENABLE KEYS")
    cursor.execute("ALTER TABLE playlist_tracks ENABLE KEYS")

    print("🛠 Début de l'optimisation des tables")
