import sys
import os

# Ajouter le chemin du répertoire racine du projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, HTTPException
from app.api.v1.alert import recommandation_vetements, previsions_meteo, infos_ville, qualite_air,previsions_horaires
import gradio as gr

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Météo !"}

@app.get("/recommandation/{city}")
def get_recommandation(city: str):
    try:
        print("Votre ville selectionnée : " +city )
        recommendation = recommandation_vetements(city)
        if recommendation is None:
            raise HTTPException(status_code=400, detail="Erreur : Impossible de récupérer les données météorologiques.")
        return {"city": city, "recommendation": recommendation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/previsions/{city}/{days}")
def get_previsions(city: str, days: int):
    try:
        print("Votre ville selectionnée : " +city )
        forecasts = previsions_meteo(city, days)
        if forecasts is None:
            raise HTTPException(status_code=400, detail="Erreur : Impossible de récupérer les prévisions météorologiques.")
        return {"city": city, "forecasts": forecasts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/infos/{city}")
def get_infos(city: str):
    try:
        print("Votre ville selectionnée : " +city )
        info = infos_ville(city)
        if info is None:
            raise HTTPException(status_code=400, detail="Erreur : Impossible de récupérer les informations de la ville.")
        return {"city": city, "info": info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/qualite_air/{city}")
def get_infos(city: str):
    try:
        print("Votre ville selectionnée : " +city )
        info = qualite_air(city)
        if info is None:
            raise HTTPException(status_code=400, detail="Erreur : Impossible de récupérer les informations de la ville.")
        return {"city": city, "info": info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
  
@app.get("/previsions_horaires/{city}")
def get_infos(city: str):
    try:
        print("Votre ville selectionnée : " +city )
        info = previsions_horaires(city)
        if info is None:
            raise HTTPException(status_code=400, detail="Erreur : Impossible de récupérer les informations de la ville.")
        return {"city": city, "info": info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
  


# Gradio Interface Functions
def gradio_recommandation(city):
    try:
        recommendation = recommandation_vetements(city)
        if recommendation is None:
            return "<div style='color: red;'>Erreur : Impossible de récupérer les données météorologiques.</div>"
        
        result = f"""
        <div style="border: 1px solid #ccc; padding: 20px; margin: 20px; border-radius: 10px; font-family: Arial, sans-serif;">
            <h2>Recommandation pour {city}</h2>
            <p>{recommendation}</p>
        </div>
        """
        return result
    except Exception as e:
        return f"<div style='color: red;'>Erreur : {str(e)}</div>"


def gradio_previsions(city, days):
    previsions = previsions_meteo(city, days)
    if previsions is None:
        return "Désolé, impossible de récupérer les prévisions météorologiques pour cette ville."

    result = ""
    for day in previsions:
        date = day['date']
        day_info = day['day']
        condition = day_info['condition']['text']
        icon_url = day_info['condition']['icon']
        max_temp = day_info['maxtemp_c']
        min_temp = day_info['mintemp_c']
        avg_temp = day_info['avgtemp_c']
        result += f"""
        <div style="border: 1px solid #ccc; padding: 10px; margin: 10px; border-radius: 5px;">
            <h3>Date: {date}</h3>
            <p><img src="{icon_url}" alt="{condition}" style="vertical-align:middle;"> {condition}</p>
            <p>Température max: <strong>{max_temp}°C</strong></p>
            <p>Température min: <strong>{min_temp}°C</strong></p>
            <p>Température moyenne: <strong>{avg_temp}°C</strong></p>
        </div>
        """
    
    return result

def gradio_infos(city):
    try:
        info = infos_ville(city)
        if info is None:
            return "<div style='color: red;'>Erreur : Impossible de récupérer les informations de la ville.</div>"
        
        city_name = info['name']
        region = info['region']
        country = info['country']
        local_time = info['localtime']
        lat = info['lat']
        lon = info['lon']

        result = f"""
        <div style="border: 1px solid #ccc; padding: 20px; margin: 20px; border-radius: 10px; font-family: Arial, sans-serif;">
            <h2>Informations sur {city_name}</h2>
            <p><strong>Région :</strong> {region}</p>
            <p><strong>Pays :</strong> {country}</p>
            <p><strong>Heure locale :</strong> {local_time}</p>
            <p><strong>Latitude :</strong> {lat}</p>
            <p><strong>Longitude :</strong> {lon}</p>
        </div>
        """
        return result
    except Exception as e:
        return f"<div style='color: red;'>Erreur : {str(e)}</div>"


def gradio_air_quality(city):
    try:
        air_quality = qualite_air(city)
        if air_quality is None:
            return "<div style='color: red;'>Erreur : Impossible de récupérer les données de qualité de l'air.</div>"
        
        pm10 = air_quality.get('pm10', 'N/A')
        pm2_5 = air_quality.get('pm2_5', 'N/A')
        no2 = air_quality.get('no2', 'N/A')
        o3 = air_quality.get('o3', 'N/A')
        so2 = air_quality.get('so2', 'N/A')
        co = air_quality.get('co', 'N/A')

        result = f"""
        <div style="border: 1px solid #ccc; padding: 20px; margin: 20px; border-radius: 10px; font-family: Arial, sans-serif;">
            <h2>Qualité de l'air à {city}</h2>
            <p><strong>PM10 :</strong> {pm10}</p>
            <p><strong>PM2.5 :</strong> {pm2_5}</p>
            <p><strong>NO2 (Dioxyde d'azote) :</strong> {no2}</p>
            <p><strong>O3 (Ozone) :</strong> {o3}</p>
            <p><strong>SO2 (Dioxyde de soufre) :</strong> {so2}</p>
            <p><strong>CO (Monoxyde de carbone) :</strong> {co}</p>
        </div>
        """
        return result
    except Exception as e:
        return f"<div style='color: red;'>Erreur : {str(e)}</div>"


# Gradio Interface Functions
def gradio_hourly_forecast(city):
    try:
        forecast = previsions_horaires(city)
        if forecast is None:
            return "<div style='color: red;'>Erreur : Impossible de récupérer les prévisions météorologiques.</div>"
        
        result = f"""
        <div style="border: 1px solid #ccc; padding: 20px; margin: 20px; border-radius: 10px; font-family: Arial, sans-serif;">
            <h2>Prévisions Météo Horaires pour {city}</h2>
        """
        for hour in forecast[::2]:  # Afficher les prévisions toutes les 2 heures
            time = hour['time']
            condition = hour['condition']['text']
            temp = hour['temp_c']
            icon_url = hour['condition']['icon']
            result += f"""
            <div style='margin-bottom: 20px;'>
                <h3>{time}</h3>
                <p><img src='{icon_url}' alt='{condition}' style='vertical-align:middle;'> {condition}</p>
                <p>Température : {temp}°C</p>
            </div>
            """
        result += "</div>"
        return result
    except Exception as e:
        return f"<div style='color: red;'>Erreur : {str(e)}</div>"




# Gradio Interface Setup

#iface1 = gr.Interface(fn=gradio_recommandation, inputs="text", outputs="text", title="Recommandation de Vêtements")

iface1 = gr.Interface(
    fn=gradio_recommandation,
    inputs=["text"],
    outputs=gr.HTML(),
    title="Recommandation de Vêtements Météo"
)
iface2 = gr.Interface(
    fn=gradio_previsions,
    inputs=["text", "number"],
    outputs=gr.HTML(),
    title="Prévisions Météo"
)
iface3 = gr.Interface(
    fn=gradio_infos,
    inputs=["text"],
    outputs=gr.HTML(),
    title="Informations sur la Ville"
)

iface4 = gr.Interface(
    fn=gradio_air_quality,
    inputs=["text"],
    outputs=gr.HTML(),
    title="Qualité de l'air"
)
iface5 = gr.Interface(
    fn=gradio_hourly_forecast,
    inputs=["text"],
    outputs=gr.HTML(),
    title="Prévisions Météo Horaires"
)

iface = gr.TabbedInterface([iface1, iface2, iface3, iface4, iface5], ["Recommandation", "Prévisions", "Informations", "Qualité de l'air","Prévisions Aujourd'hui"])


if __name__ == "__main__":
    iface.launch()

