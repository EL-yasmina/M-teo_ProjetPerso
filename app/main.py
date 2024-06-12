from fastapi import FastAPI, HTTPException
from app.api.v1.alert import recommandation_vetements 

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Météo !"}

@app.get("/recommandation/{city}")
def get_recommandation(city: str):
    try:
        recommendation = recommandation_vetements(city)
        if recommendation.startswith("Erreur"):
            raise HTTPException(status_code=400, detail=recommendation)
        return {"city": city, "recommendation": recommendation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
