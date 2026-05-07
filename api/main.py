from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel


MODEL_PATH = Path("/data/models/model.joblib")

app = FastAPI(title="ML Serving Stack API")


class PredictionRequest(BaseModel):
    features: list[float]


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_exists": MODEL_PATH.exists()
    }


@app.post("/predict")
def predict(request: PredictionRequest):
    model = joblib.load(MODEL_PATH)

    features = np.array(request.features).reshape(1, -1)
    prediction = model.predict(features)

    return {
        "prediction": int(prediction[0])
    }