import os

# Constants for UrbanFlux AI

PRODUCT_TYPES = ['Tomato', 'Milk', 'Onion', 'Meat', 'Fish']
QUALITY_GRADES = ['A', 'B', 'C']
STORAGE_TYPES = ['Ambient', 'Refrigerated']
CONGESTION_LEVELS = ['Low', 'Medium', 'High']
RISK_LEVELS = ['Low', 'Medium', 'High']

# Base directory for absolute path resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Model Paths (absolute)
MODEL_DIR = os.path.join(PROJECT_ROOT, "models")
FRESHNESS_MODEL_PATH = os.path.join(MODEL_DIR, "freshness_model.pkl")
SPOILAGE_MODEL_PATH = os.path.join(MODEL_DIR, "spoilage_risk_model.pkl")
PRIORITY_MODEL_PATH = os.path.join(MODEL_DIR, "priority_score_model.pkl")

# Data Paths (absolute)
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "merged_training_data.csv")
