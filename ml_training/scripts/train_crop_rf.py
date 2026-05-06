"""
Random Forest Model for Crop Recommendation
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../../backend/app/ml/models")
os.makedirs(MODEL_DIR, exist_ok=True)

def load_soil_crop_data():
    """Load soil-crop suitability data"""
    df = pd.read_csv(os.path.join(DATA_DIR, "soil_crop_data.csv"))
    return df

def preprocess_data(df):
    """Preprocess data for training"""
    # Encode categorical variables
    soil_encoder = LabelEncoder()
    season_encoder = LabelEncoder()
    crop_encoder = LabelEncoder()
    
    df['soil_encoded'] = soil_encoder.fit_transform(df['soil_type'])
    df['season_encoded'] = season_encoder.fit_transform(df['season'])
    df['crop_encoded'] = crop_encoder.fit_transform(df['recommended_crop'])
    
    # Features
    feature_cols = ['soil_encoded', 'season_encoded', 'rainfall_mm', 
                    'temperature_c', 'ph', 'nitrogen', 'phosphorus', 'potassium']
    
    X = df[feature_cols].values
    y = df['crop_encoded'].values
    
    return X, y, soil_encoder, season_encoder, crop_encoder

def train_crop_model():
    """Train Random Forest model for crop recommendation"""
    print("=" * 60)
    print("Random Forest Crop Recommendation Model Training")
    print("=" * 60)
    
    # Load data
    df = load_soil_crop_data()
    print(f"\nLoaded {len(df)} records")
    print(f"Crops: {df['recommended_crop'].unique()}")
    
    # Preprocess
    X, y, soil_encoder, season_encoder, crop_encoder = preprocess_data(df)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Train Random Forest
    print("\nTraining Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nTest Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(
        y_test, y_pred, 
        target_names=crop_encoder.classes_
    ))
    
    # Cross-validation
    cv_scores = cross_val_score(model, X, y, cv=5)
    print(f"\nCross-validation scores: {cv_scores}")
    print(f"Mean CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Feature importance
    feature_names = ['soil', 'season', 'rainfall', 'temperature', 
                     'ph', 'nitrogen', 'phosphorus', 'potassium']
    importance = model.feature_importances_
    
    print("\nFeature Importance:")
    for name, imp in sorted(zip(feature_names, importance), key=lambda x: x[1], reverse=True):
        print(f"  {name}: {imp:.4f}")
    
    # Save model and encoders
    joblib.dump(model, os.path.join(MODEL_DIR, 'crop_recommendation_rf.pkl'))
    joblib.dump(soil_encoder, os.path.join(MODEL_DIR, 'soil_encoder.pkl'))
    joblib.dump(season_encoder, os.path.join(MODEL_DIR, 'season_encoder.pkl'))
    joblib.dump(crop_encoder, os.path.join(MODEL_DIR, 'crop_encoder.pkl'))
    
    print(f"\nModels saved to: {MODEL_DIR}")
    
    return model, soil_encoder, season_encoder, crop_encoder

def predict_crop(model, encoders, soil_type, season, rainfall, temperature, ph, n, p, k):
    """Predict best crop for given conditions"""
    soil_encoder, season_encoder, crop_encoder = encoders
    
    # Encode inputs
    try:
        soil_encoded = soil_encoder.transform([soil_type])[0]
    except:
        soil_encoded = 0  # Default
    
    try:
        season_encoded = season_encoder.transform([season])[0]
    except:
        season_encoded = 0  # Default
    
    # Create feature vector
    features = np.array([[soil_encoded, season_encoded, rainfall, 
                          temperature, ph, n, p, k]])
    
    # Predict
    pred_encoded = model.predict(features)[0]
    pred_proba = model.predict_proba(features)[0]
        
    # Decode
    predicted_crop = crop_encoder.inverse_transform([pred_encoded])[0]
    confidence = pred_proba[pred_encoded]
    
    # Get top 3 predictions
    top_indices = np.argsort(pred_proba)[-3:][::-1]
    top_crops = crop_encoder.inverse_transform(top_indices)
    top_probs = pred_proba[top_indices]
    
    return {
        'recommended_crop': predicted_crop,
        'confidence': confidence,
        'alternatives': list(zip(top_crops, top_probs))
    }

if __name__ == "__main__":
    # Check if data exists
    data_file = os.path.join(DATA_DIR, "soil_crop_data.csv")
    if not os.path.exists(data_file):
        print(f"Data file not found: {data_file}")
        print("Please run generate_sample_data.py first.")
        exit(1)
    
    # Train model
    model, soil_encoder, season_encoder, crop_encoder = train_crop_model()
    
    # Test prediction
    print("\n" + "=" * 60)
    print("Testing prediction...")
    print("=" * 60)
    
    result = predict_crop(
        model, 
        (soil_encoder, season_encoder, crop_encoder),
        soil_type="Black Soil",
        season="Kharif",
        rainfall=800,
        temperature=28,
        ph=6.5,
        n=150,
        p=50,
        k=100
    )
    
    print(f"\nPredicted Crop: {result['recommended_crop']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print("\nTop 3 Recommendations:")
    for crop, prob in result['alternatives']:
        print(f"  {crop}: {prob:.2%}")
