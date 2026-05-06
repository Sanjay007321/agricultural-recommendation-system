"""
Evaluation script for Disease Risk Model
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../../backend/app/ml/models")
os.makedirs(MODEL_DIR, exist_ok=True)

def evaluate_disease_model():
    print("=" * 60)
    print("Disease Risk Model Evaluation (Random Forest)")
    print("=" * 60)
    
    # Load data
    df = pd.read_csv(os.path.join(DATA_DIR, "disease_data.csv"))
    print(f"\nLoaded {len(df)} records")
    
    # Preprocess
    crop_encoder = LabelEncoder()
    season_encoder = LabelEncoder()
    disease_encoder = LabelEncoder()
    
    df['crop_encoded'] = crop_encoder.fit_transform(df['crop'])
    df['season_encoded'] = season_encoder.fit_transform(df['season'])
    df['disease_encoded'] = disease_encoder.fit_transform(df['disease_occurred'])
    
    # Features
    features = ['crop_encoded', 'season_encoded', 'humidity_percent', 'temperature_c', 'rainfall_mm']
    
    X = df[features]
    y = df['disease_encoded']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nTest Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=disease_encoder.classes_))
    
    # Feature Importance
    importance = model.feature_importances_
    for name, imp in sorted(zip(features, importance), key=lambda x: x[1], reverse=True):
        print(f"  {name}: {imp:.4f}")
        
    # Save model
    joblib.dump(model, os.path.join(MODEL_DIR, 'disease_prediction_rf.pkl'))
    print(f"\nModel saved to: {MODEL_DIR}")

if __name__ == "__main__":
    evaluate_disease_model()
