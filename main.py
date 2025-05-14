from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict
import joblib
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize FastAPI app
app = FastAPI(title="IMK Prediction API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
model = joblib.load("model/xgb_model.pkl")

# Define constants
REQUIRED_FEATURES = [
    "Umur",
    "JenisKelamin",
    "TinggiBadan",
]

# Define request model
class PredictionInput(BaseModel):
    """Input model for prediction request."""
    Umur: int = Field(..., alias="Umur (bulan)")
    JenisKelamin: int = Field(..., alias="Jenis Kelamin")
    TinggiBadan: int = Field(..., alias="Tinggi Badan (cm)")


# Define response model
class PredictionResponse(BaseModel):
    Status_Gizi: int
    confidence: float


def generate_prediction(input_data: List[float]) -> tuple[int, float]:
    """Generate prediction and confidence score."""
    Status_Gizi = int(model.predict([input_data])[0])
    confidence = float(model.predict_proba([input_data])[0][Status_Gizi])
    return Status_Gizi, confidence


@app.get("/")
async def home():
    """Root endpoint."""
    return {"message": "Welcome to the ML Prediction API!"}


@app.post("/predict", response_model=PredictionResponse)
async def predict(input_data: PredictionInput):
    """
    Make a prediction based on the input features.
    Returns prediction and confidence score.
    """
    try:
        # Convert input data to list in correct order
        input_values = [getattr(input_data, feature) for feature in REQUIRED_FEATURES]

        # Generate prediction
        prediction_value, confidence_value = generate_prediction(input_values)

        return PredictionResponse(
            Status_Gizi=prediction_value, confidence=round(confidence_value, 3)
        )

    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
