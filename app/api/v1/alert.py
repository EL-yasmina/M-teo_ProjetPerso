import requests
import json
import os
import tkinter as tk
from tkinter import simpledialog

api_key = "61064c6295144de9b63101812242904"
def sauvegarder_donneesCurrent_json(donnees, nom_fichier, dossier):
    """
    Sauvegarde les données dans un fichier JSON.

    Args:
        donnees (dict): Les données à sauvegarder.
        nom_fichier (str): Le nom du fichier JSON de sortie.
    """
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
        sauvegarder_donneesCurrent_json(data, "currentMet_"+city+".json", "dataa")

        # Extraire les informations pertinentes des données JSON
        temperature_celsius = data['current']['temp_c']
        condition = data['current']['condition']['text']
        precipitation_mm = data['current']['precip_mm']

        # Déterminer la recommandation de vêtements en fonction de la température et des conditions météorologiques
        if temperature_celsius < 10:
            return "Il fait plutôt frais à {} avec {}°C. Tu devrais peut-être envisager de porter quelque chose de chaud !".format(data['location']['name'], temperature_celsius)
        elif temperature_celsius >= 10 and temperature_celsius < 20:
            if precipitation_mm > 0:
                return "Il y a {} à {} et il fait {}°C. Prends un parapluie et peut-être un pull léger !".format(condition, data['location']['name'], temperature_celsius)
            else:
                return "À {} il fait {}°C, un t-shirt et une veste légère pourraient être parfaits pour toi !".format(data['location']['name'], temperature_celsius)
        else:
            if precipitation_mm > 0:
                return "Il pleut à {} et il fait {}°C. N'oublie pas ton parapluie !".format(data['location']['name'], temperature_celsius)
            else:
                return "Il fait chaud à {} avec {}°C. C'est le moment de sortir les shorts et les lunettes de soleil !".format(data['location']['name'], temperature_celsius)
    else:
        # Si la requête a échoué, retourner None
        return None
# Création de la fenêtre principale
root = tk.Tk()
# Masquer la fenêtre principale
root.withdraw()  

# Afficher une boîte de dialogue avec un champ de saisie
user_input = simpledialog.askstring("Meteo ville", "Entrez votre ville ici :")

message = recommandation_vetements(user_input)

# Afficher le texte saisi
if message is not None:
    tk.messagebox.showinfo("Information", message)

else:
    tk.messagebox.showinfo("Information", "Vous êtes sûr que c'est la bonne ville !")

# Fermer la fenêtre
root.destroy()
