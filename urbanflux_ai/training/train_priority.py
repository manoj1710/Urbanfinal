import pandas as pd
import joblib
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.constants import PRIORITY_MODEL_PATH, PROCESSED_DATA_PATH

def train_priority_model():
    print("Training Priority Scoring Model (XGBoost)...")
    
    if not os.path.exists(PROCESSED_DATA_PATH):
        print(f"Error: {PROCESSED_DATA_PATH} not found.")
        return

    df = pd.read_csv(PROCESSED_DATA_PATH)
    
    features = ['spoilage_risk', 'demand_score', 'distance_km']
    target = 'priority_score'
    
    X = df[features]
    y = df[target]
    
    categorical_features = ['spoilage_risk']
    numerical_features = ['demand_score', 'distance_km']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    regressor = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, seed=42)
    
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', regressor)
    ])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model.fit(X_train, y_train)
    
    os.makedirs(os.path.dirname(PRIORITY_MODEL_PATH), exist_ok=True)
    joblib.dump(model, PRIORITY_MODEL_PATH)
    print(f"Model saved to {PRIORITY_MODEL_PATH}")

if __name__ == "__main__":
    train_priority_model()
