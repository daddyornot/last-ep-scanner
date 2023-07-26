import os
from collections import defaultdict
import re

series_directory = "chemin du dossier contenant les series"
series_file_path = "series_a_suivre.txt"

# Vérifie si le fichier des séries à suivre existe
if os.path.exists(series_file_path):
    # Charge les séries à suivre à partir du fichier
    with open(series_file_path, "r") as file:
        series_a_suivre = [serie.strip() for serie in file.readlines()]
else:
    # Demande à l'utilisateur de saisir les séries à suivre, séparées par des virgules
    series_a_suivre_str = input("Entrez les séries à suivre (séparées par des virgules): ")
    series_a_suivre = [serie.strip() for serie in series_a_suivre_str.split(",")]

    # Enregistre les séries dans le fichier
    with open(series_file_path, "w") as file:
        file.write("\n".join(series_a_suivre))

# Dictionnaire pour stocker les derniers fichiers de chaque série
derniers_episodes = defaultdict(lambda: {"saison": 0, "episode": 0})

# Parcours récursif de tous les fichiers et dossiers dans le répertoire de séries
for root, dirs, files in os.walk(series_directory):
    for file in files:
        # Vérification de l'extension du fichier (.mkv ou .mp4)
        if file.endswith((".mkv", ".mp4")):
            # Obtention du chemin complet du fichier
            chemin_fichier = os.path.join(root, file)

            # Extraction des informations du nom du fichier (série, saison, épisode)
            serie = None
            saison, episode = None, None

            # Recherche des informations dans le nom du fichier en utilisant des expressions régulières
            match = re.search(r"\\([^\\]+)\\Season\s*(\d+)\\.*?[-_.x]\s*(\d+)", chemin_fichier)
            if match:
                serie = match.group(1)
                saison = int(match.group(2))
                episode = int(match.group(3))

                # Vérification si le numéro de saison est plus grand ou le même, et si le numéro d'épisode est plus grand
                if episode is not None and saison >= derniers_episodes[serie]["saison"]:
                    # Vérification si la série fait partie des séries à suivre
                    if serie in series_a_suivre:
                        derniers_episodes[serie]["saison"] = saison
                        derniers_episodes[serie]["episode"] = episode


# Affichage des derniers épisodes de chaque série à suivre
print(f"\n{'='*20}\nDerniers épisodes\n{'='*20}\n")
for serie in series_a_suivre:
    dernier_episode = derniers_episodes[serie]["episode"]
    dernier_saison = derniers_episodes[serie]["saison"]
    if dernier_episode == 0 and dernier_saison == 0:
        print(f"\n{'='*40}\nAucun épisode trouvé pour la série {serie}\n{'='*40}")
    else:
        print(f"{'='*20} {serie} {'='*20}\n Saison {dernier_saison}, Épisode {dernier_episode}\n{'='*40}\n")


input("Appuyer sur entrée pour quitter...")