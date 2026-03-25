# AI-Based Phishing Detection System 🛡️🤖

An intelligent, secure, and cloud-ready phishing detection system built for the **Cloud Architecture and Security** course (NSY107).

## 🚀 Overview
This project provides an end-to-end solution for detecting phishing attempts in emails or URLs. It combines machine learning with a secure cloud API and a modern web frontend.

## 🏗️ Project Components
- **ML Pipeline**: Uses `scikit-learn` with an SVM classifier and `TF-IDF` vectorization to achieve high accuracy.
- **Secure API**: Built with `FastAPI`, featuring CORS support and API Key authentication for simulated cloud security.
- **Modern Frontend**: A clean HTML/JS interface that interacts with the backend in real-time.
- **Cloud-Ready**: Includes a `Dockerfile` for seamless deployment to platforms like AWS, Google Cloud, or Render.

## 📁 Project Structure
```
/AI-Phishing-Detection-System
|-- CEAS_08.csv             # Dataset for training
|-- train_model.py          # Script to train and export the model
|-- app.py                  # FastAPI backend server
|-- index.html              # Web frontend
|-- requirements.txt        # Python dependencies
|-- Dockerfile              # Docker container configuration
|-- .gitignore              # Files to exclude from Git
```

## 🛠️ Installation & Usage

### 1. Train the Model
```bash
python train_model.py
```
This generates `model.pkl` and `vectorizer.pkl`.

### 2. Run the API Server
```bash
python app.py
```
The server will start at `http://127.0.0.1:8000`.

### 3. Open the Frontend
Open `index.html` in your browser and start analyzing!

## 🔐 Security Note
The API is protected with an API Key (`X-API-Key`). For local testing, use the default key: `your_secret_api_key`.

## 🐳 Docker Deployment
```bash
docker build -t phishing-detector .
docker run -p 8000:8000 phishing-detector
```

---
**Course**: NSY107 - Cloud Architecture and Security
**Developer**: Mahdi Haida
