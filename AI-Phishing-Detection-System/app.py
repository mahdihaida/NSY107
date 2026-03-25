
import pickle
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# --- API Key Security ---
API_KEY = "your_secret_api_key"  # In a real-world app, use environment variables!
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )

# --- FastAPI App ---
app = FastAPI(
    title="Phishing Detection API",
    description="An API to detect phishing attempts in text using an SVM model.",
    version="1.0.0"
)

# --- Fix for CORS (405 Method Not Allowed) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For university project, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ML Model Loading ---
model = None
vectorizer = None

def load_models():
    global model, vectorizer
    try:
        with open('model.pkl', 'rb') as model_file:
            model = pickle.load(model_file)
        with open('vectorizer.pkl', 'rb') as vectorizer_file:
            vectorizer = pickle.load(vectorizer_file)
    except FileNotFoundError:
        print("Model or vectorizer not found. Please run train_model.py first.")

load_models()

class AnalysisRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    prediction: str
    confidence: float

@app.post("/analyze", response_model=AnalysisResponse, dependencies=[Depends(get_api_key)])
def analyze_text(request: AnalysisRequest):
    """
    Analyzes a given text for phishing attempts.
    Requires a valid API key in the `X-API-Key` header.
    """
    if model is None or vectorizer is None:
        load_models()
        if model is None or vectorizer is None:
            raise HTTPException(status_code=500, detail="Models not loaded on server.")

    # Preprocess the input text
    text_tfidf = vectorizer.transform([request.text])

    # Make prediction and get confidence score
    prediction_label = model.predict(text_tfidf)[0]
    confidence = model.predict_proba(text_tfidf).max()

    result = "Phishing" if prediction_label == 1 else "Safe"

    return {"prediction": result, "confidence": confidence}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
