"""
Evaluation script for Yield Prediction Model
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../../backend/app/ml/models")
os.makedirs(MODEL_DIR, exist_ok=True)

def evaluate_yield_model():
    print("=" * 60)
    print("Yield Prediction Model Evaluation (Random Forest)")
    print("=" * 60)
    
    # Load data
    df = pd.read_csv(os.path.join(DATA_DIR, "crop_yields.csv"))
    print(f"\nLoaded {len(df)} records")
    
    # Preprocess
    crop_encoder = LabelEncoder()
    state_encoder = LabelEncoder()
    season_encoder = LabelEncoder()
    soil_encoder = LabelEncoder()
    
    df['crop_encoded'] = crop_encoder.fit_transform(df['crop'])
    df['state_encoded'] = state_encoder.fit_transform(df['state'])
    df['season_encoded'] = season_encoder.fit_transform(df['season'])
    df['soil_encoded'] = soil_encoder.fit_transform(df['soil_type'])
    
    features = ['crop_encoded', 'state_encoded', 'season_encoded', 'soil_encoded',
                'rainfall_mm', 'temperature_c', 'ph', 'nitrogen', 'phosphorus', 'potassium']
    
    X = df[features]
    y = df['yield_per_acre']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nMean Absolute Error: {mae:.4f}")
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"R² Score: {r2:.4f}")
    
    # Feature Importance
    importance = model.feature_importances_
    for name, imp in sorted(zip(features, importance), key=lambda x: x[1], reverse=True):
        print(f"  {name}: {imp:.4f}")
        
    # Save model
    joblib.dump(model, os.path.join(MODEL_DIR, 'yield_prediction_rf.pkl'))
    print(f"\nModel saved to: {MODEL_DIR}")

if __name__ == "__main__":
    evaluate_yield_model()
