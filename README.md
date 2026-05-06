# Crop Management & Profit Analysis System

A comprehensive web application designed for Indian farmers to manage crops, analyze soil, and predict profits using machine learning.

## Features

- **Soil Analysis**: Upload soil images to get nutrient composition and crop suitability (Demo mode included).
- **Crop Recommendation**: ML-based recommendations based on soil, climate, and region.
- **Profit Prediction**: Predict potential profits based on current market rates and historical data.
- **Weather Integration**: Real-time weather data from IMD APIs.
- **Irrigation Guidance**: Specialized recommendations for irrigation management.
- **Multilingual Support**: (Voice input and chatbot features).

## Tech Stack

- **Frontend**: React (Vite), Tailwind CSS, Framer Motion, Recharts.
- **Backend**: FastAPI (Python), SQLAlchemy, SQLite.
- **Machine Learning**: Scikit-learn, PyTorch (Optional for enhanced image processing).
- **Deployment**: Docker, Docker Compose.

## Quick Start (Local Run)

If you have Python and Node.js installed, you can run the app without Docker:

### 1. Backend
```bash
cd backend
python -m venv venv
# Activate venv: .\venv\Scripts\activate (Windows) or source venv/bin/activate (Linux/Mac)
pip install -r requirements.txt
python main.py
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```

## Deployment with Docker

Ensure Docker Desktop is running and run:
```bash
docker-compose up --build -d
```

## Documentation
For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## License
MIT
