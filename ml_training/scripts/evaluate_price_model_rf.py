"""
Fallback Evaluation script for Price Prediction Model (Random Forest)
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../../backend/app/ml/models")
os.makedirs(MODEL_DIR, exist_ok=True)

def evaluate_price_model():
    print("=" * 60)
    print("Price Prediction Model Evaluation (Random Forest Fallback)")
    print("=" * 60)
    
    # Load data
    df = pd.read_csv(os.path.join(DATA_DIR, "crop_prices.csv"))
    print(f"\nLoaded {len(df)} records")
    
    # For price prediction from historical data, we need a simple lag model
    # Let's take 'Rice' as an example
    df_rice = df[df['crop'] == 'Rice'].copy()
    df_rice['date'] = pd.to_datetime(df_rice['date'])
    df_rice = df_rice.sort_values('date')
    
    # Create lag features
    for i in range(1, 8):
        df_rice[f'lag_{i}'] = df_rice['price_per_quintal'].shift(i)
        
    df_rice = df_rice.dropna()
    
    X = df_rice[[f'lag_{i}' for i in range(1, 8)]]
    y = df_rice['price_per_quintal']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    # Train
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nMetrics for Rice Price Prediction:")
    print(f"  Mean Absolute Error: {mae:.4f}")
    print(f"  Mean Squared Error: {mse:.4f}")
    print(f"  R² Score: {r2:.4f}")
    
    # Save model
    joblib.dump(model, os.path.join(MODEL_DIR, 'price_prediction_rf_rice.pkl'))
    print(f"\nModel saved to: {MODEL_DIR}")

if __name__ == "__main__":
    evaluate_price_model()
