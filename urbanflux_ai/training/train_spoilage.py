import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.constants import SPOILAGE_MODEL_PATH, PROCESSED_DATA_PATH

def train_spoilage_model():
    print("Training Spoilage Risk Model (Random Forest Classifier)...")
    
    if not os.path.exists(PROCESSED_DATA_PATH):
        print(f"Error: {PROCESSED_DATA_PATH} not found.")
        return

    df = pd.read_csv(PROCESSED_DATA_PATH)
    
    features = ['current_freshness', 'delay_factor', 'temperature', 'congestion_level']
    target = 'spoilage_risk'
    
    X = df[features]
    y = df[target]
    
    categorical_features = ['congestion_level']
    numerical_features = ['current_freshness', 'delay_factor', 'temperature']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model.fit(X_train, y_train)
    
    os.makedirs(os.path.dirname(SPOILAGE_MODEL_PATH), exist_ok=True)
    joblib.dump(model, SPOILAGE_MODEL_PATH)
    print(f"Model saved to {SPOILAGE_MODEL_PATH}")

if __name__ == "__main__":
    train_spoilage_model()
