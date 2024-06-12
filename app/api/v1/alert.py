import requests
import json
import os
# import tkinter as tk
# from tkinter import simpledialog

api_key = "c505f918cd1244f9a5d132545241206"

def sauvegarder_donneesCurrent_json(donnees, nom_fichier, dossier):
    """
    Sauvegarde les données dans un fichier JSON.

    Args:
        donnees (dict): Les données à sauvegarder.
        nom_fichier (str): Le nom du fichier JSON de sortie.
        dossier (str): Le dossier où sauvegarder le fichier.
    """
    os.makedirs(dossier, exist_ok=True)  # Créer le dossier s'il n'existe pas
    chemin = os.path.join(dossier, nom_fichier)
    with open(chemin, "w") as json_file:
        json.dump(donnees, json_file, indent=4)

def recommandation_vetements(city):
    """
    Donne une recommandation de vêtements en fonction des conditions météorologiques.

    Args:
        city (str): Le nom de la ville pour laquelle obtenir la recommandation.

    Returns:
        str: La recommandation de vêtements basée sur les conditions météorologiques.
    """
    # URL de l'API pour les données
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    # Faire une requête GET pour obtenir les données
    response = requests.get(url)
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Convertir la réponse en format JSON
        data = response.json()

        # Sauvegarder les données météorologiques actuelles dans un fichier JSON
        sauvegarder_donneesCurrent_json(data, "currentMet_"+city+".json", "data")

        # Extraire les informations pertinentes des données JSON
        temperature_celsius = data['current']['temp_c']
        condition = data['current']['condition']['text']
        precipitation_mm = data['current']['precip_mm']

        # Déterminer la recommandation de vêtements en fonction de la température et des conditions météorologiques
        if temperature_celsius < 10:
            return f"Il fait plutôt frais à {data['location']['name']} avec {temperature_celsius}°C. Tu devrais peut-être envisager de porter quelque chose de chaud !"
        elif 10 <= temperature_celsius < 20:
            if precipitation_mm > 0:
                return f"Il y a {condition} à {data['location']['name']} et il fait {temperature_celsius}°C. Prends un parapluie et peut-être un pull léger !"
            else:
                return f"À {data['location']['name']} il fait {temperature_celsius}°C, un t-shirt et une veste légère pourraient être parfaits pour toi !"
        else:
            if precipitation_mm > 0:
                return f"Il pleut à {data['location']['name']} et il fait {temperature_celsius}°C. N'oublie pas ton parapluie !"
            else:
                return f"Il fait chaud à {data['location']['name']} avec {temperature_celsius}°C. C'est le moment de sortir les shorts et les lunettes de soleil !"
    else:
        return None

# Commenter la partie Tkinter pour se concentrer sur FastAPI
# Création de la fenêtre principale
# root = tk.Tk()
# Masquer la fenêtre principale
# root.withdraw()  

# Afficher une boîte de dialogue avec un champ de saisie
# user_input = simpledialog.askstring("Meteo ville", "Entrez votre ville ici :")

# message = recommandation_vetements(user_input)

# Afficher le texte saisi
# if message is not None:
#     tk.messagebox.showinfo("Information", message)

# else:
#     tk.messagebox.showinfo("Information", "Vous êtes sûr que c'est la bonne ville !")

# Fermer la fenêtre
# root.destroy()
