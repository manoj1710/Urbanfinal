# UrbanFlux AI Backend

A production-ready Python-based AI microservice for the UrbanFlux supply chain optimization platform.
This service generates synthetic data, trains explainable ML models, and exposes REST APIs for logistics intelligence.

## 📂 Project Structure

```
urbanflux_ai/
├── main.py                     # FastAPI Application Entry Point
├── requirements.txt            # Python Dependencies (pinned versions)
├── data/                       # CSV Data Storage (local training only)
│   ├── raw/                    # Generated Synthetic Data
│   └── processed/              # Merged Training Data
├── models/                     # Trained .pkl Models
├── training/                   # ML Training Scripts (local setup)
│   ├── generate_data.py        # Data Generator
│   ├── train_*.py              # Individual Model Trainers
│   └── train_all.py            # Master Training Pipeline
├── services/                   # Business Logic & Inference
└── utils/                      # Shared Utilities
```

## 🚀 Local Setup & Installation

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🧠 Data Generation & Model Training (Local Only)

To set up the AI engine locally, you must first generate data and train the models.
**Note:** This step is only for local development. Models should be pre-trained before deployment.

```bash
# Runs data generation, preprocessing, and training for all models
python training/train_all.py
```

## ⚡ Running the API Locally

Start the FastAPI server:

```bash
# Default port 8000
python main.py

# Or with uvicorn directly
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`.

## 📡 API Endpoints

- `GET /health` - Health check with timestamp
- `POST /ai/freshness` - Predict product freshness
- `POST /ai/spoilage-risk` - Predict spoilage risk level
- `POST /ai/priority-score` - Calculate delivery priority
- `POST /ai/route-analysis` - Analyze optimal route

See `http://localhost:8000/docs` for interactive Swagger UI.

## 🌐 Production Deployment (Render)

### Prerequisites
- Pre-trained models in `models/` directory
- All dependencies listed in `requirements.txt`

### Render Configuration

1. **Service Type**: Web Service
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `python main.py`
4. **Environment Variables**:
   - `PORT` - Automatically set by Render (do not configure manually)
   - `PYTHON_VERSION` - `3.11` (recommended)

### Deployment Checklist

- [x] PORT reads from environment variable
- [x] Host binding set to `0.0.0.0`
- [x] All model paths use absolute path resolution
- [x] No runtime file creation in production code
- [x] Health endpoint returns ISO timestamp
- [x] Proper logging (not print statements)
- [x] Requirements pinned to specific versions

### Health Check Endpoint

The `/health` endpoint returns:
```json
{
  "status": "OK",
  "service": "urbanflux-ai",
  "timestamp": "2026-02-10T15:27:03.123456Z"
}
```

Use this for Render health checks and monitoring.

### Model Loading Behavior

- Models are loaded at startup from the `models/` directory
- If a model fails to load, the service will still start
- API endpoints return `{"error": "Model not loaded"}` if the model is unavailable
- Check startup logs for model loading status

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8000` | Server port (auto-set by Render) |
| `BASE_URL` | `http://localhost:8000` | For verification tests only |

## 🧪 Testing

Run verification tests:

```bash
# Start server first
python main.py

# In another terminal
python verification_test.py
```

For testing against deployed service:
```bash
export BASE_URL=https://your-service.onrender.com
python verification_test.py
```

## 📝 Notes

- Training scripts (`training/`) are for local setup only
- Data generation creates local CSV files (not used in production)
- Models must be committed to the repository or uploaded separately
- Service uses graceful degradation if models fail to load
