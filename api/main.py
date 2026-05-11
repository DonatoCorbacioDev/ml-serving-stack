from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


MODEL_PATH = Path("/data/models/model.joblib")

app = FastAPI(title="ML Serving Stack API")

model = None


class PredictionRequest(BaseModel):
    features: list[float] = Field(
        ...,
        min_length=4,
        max_length=4,
        description="Four numerical features of an Iris flower"
    )


@app.on_event("startup")
def load_model():
    global model

    if not MODEL_PATH.exists():
        raise RuntimeError(f"Model file not found at {MODEL_PATH}")

    model = joblib.load(MODEL_PATH)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_exists": MODEL_PATH.exists(),
        "model_loaded": model is not None
    }


@app.post("/predict")
def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model is not loaded"
        )

    features = np.array(request.features).reshape(1, -1)
    prediction = model.predict(features)

    return {
        "prediction": int(prediction[0])
    }