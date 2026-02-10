import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.constants import FRESHNESS_MODEL_PATH, PROCESSED_DATA_PATH

def train_freshness_model():
    print("Training Freshness Model (Linear Regression)...")
    
    if not os.path.exists(PROCESSED_DATA_PATH):
        print(f"Error: {PROCESSED_DATA_PATH} not found.")
        return

    df = pd.read_csv(PROCESSED_DATA_PATH)
    
    features = ['days_in_storage', 'storage_type', 'quality_grade']
    target = 'current_freshness'
    
    X = df[features]
    y = df[target]
    
    categorical_features = ['storage_type', 'quality_grade']
    numerical_features = ['days_in_storage']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model.fit(X_train, y_train)
    
    # Save model
    os.makedirs(os.path.dirname(FRESHNESS_MODEL_PATH), exist_ok=True)
    joblib.dump(model, FRESHNESS_MODEL_PATH)
    print(f"Model saved to {FRESHNESS_MODEL_PATH}")

if __name__ == "__main__":
    train_freshness_model()
