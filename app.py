
import os
import subprocess
import pickle
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# --- ML Model Loading & Auto-Train Logic ---
model = None
vectorizer = None

def load_models():
    global model, vectorizer
    if not os.path.exists('model.pkl') or not os.path.exists('vectorizer.pkl'):
        print("Models missing! Training now...")
        try:
            subprocess.run(["python", "train_model.py"], check=True)
        except Exception as e:
            print(f"Auto-training failed: {e}")
            return

    try:
        if os.path.exists('model.pkl') and os.path.exists('vectorizer.pkl'):
            with open('model.pkl', 'rb') as model_file:
                model = pickle.load(model_file)
            with open('vectorizer.pkl', 'rb') as vectorizer_file:
                vectorizer = pickle.load(vectorizer_file)
            print("Models loaded successfully.")
    except Exception as e:
        print(f"Error loading models: {e}")

# Initial load
load_models()

# --- API Key Security ---
API_KEY = "your_secret_api_key"
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")

# --- FastAPI App ---
app = FastAPI(title="Phishing Detection API")

# VERY IMPORTANT: CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    prediction: str
    confidence: float

@app.get("/")
def home():
    return {"status": "online", "message": "Phishing Detection API is running successfully!"}

@app.post("/analyze", response_model=AnalysisResponse, dependencies=[Depends(get_api_key)])
def analyze_text(request: AnalysisRequest):
    global model, vectorizer
    if model is None or vectorizer is None:
        load_models()
        if model is None or vectorizer is None:
            raise HTTPException(status_code=500, detail="Model files not found on server.")

    try:
        text_tfidf = vectorizer.transform([request.text])
        prediction_label = model.predict(text_tfidf)[0]
        confidence = model.predict_proba(text_tfidf).max()
        result = "Phishing" if prediction_label == 1 else "Safe"
        return {"prediction": result, "confidence": float(confidence)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
