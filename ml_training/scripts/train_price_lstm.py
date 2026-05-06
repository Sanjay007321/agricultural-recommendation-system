"""
LSTM Model for Crop Price Prediction
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import os

# TensorFlow imports (will be used when training)
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow not available. Install with: pip install tensorflow")

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../../backend/app/ml/models")
os.makedirs(MODEL_DIR, exist_ok=True)

def load_price_data(crop_name: str = None):
    """Load crop price data"""
    df = pd.read_csv(os.path.join(DATA_DIR, "crop_prices.csv"))
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    if crop_name:
        df = df[df['crop'] == crop_name]
    
    return df

def create_sequences(data, seq_length=60):
    """Create sequences for LSTM training"""
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:(i + seq_length)])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

def build_lstm_model(seq_length, n_features=1):
    """Build LSTM model architecture"""
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(seq_length, n_features)),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(25),
        Dense(1)
    ])
    
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

def train_price_model(crop_name: str, seq_length: int = 60, epochs: int = 50):
    """Train LSTM model for a specific crop"""
    if not TF_AVAILABLE:
        print("TensorFlow not available. Cannot train model.")
        return None
    
    print(f"\nTraining LSTM model for {crop_name}...")
    print("-" * 50)
    
    # Load data
    df = load_price_data(crop_name)
    if len(df) < seq_length + 50:
        print(f"Not enough data for {crop_name}. Need at least {seq_length + 50} records.")
        return None
    
    prices = df['price_per_quintal'].values.reshape(-1, 1)
    
    # Scale data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)
    
    # Create sequences
    X, y = create_sequences(scaled_prices, seq_length)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )
    
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Build model
    model = build_lstm_model(seq_length)
    model.summary()
    
    # Callbacks
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
        ModelCheckpoint(
            os.path.join(MODEL_DIR, f'price_lstm_{crop_name.lower()}.h5'),
            monitor='val_loss',
            save_best_only=True
        )
    ]
    
    # Train
    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=32,
        validation_data=(X_test, y_test),
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate
    loss, mae = model.evaluate(X_test, y_test, verbose=0)
    print(f"\nTest Loss (MSE): {loss:.6f}")
    print(f"Test MAE: {mae:.6f}")
    
    # Save scaler parameters
    scaler_params = {
        'min': float(scaler.data_min_[0]),
        'max': float(scaler.data_max_[0]),
        'scale': float(scaler.scale_[0])
    }
    
    import json
    with open(os.path.join(MODEL_DIR, f'scaler_{crop_name.lower()}.json'), 'w') as f:
        json.dump(scaler_params, f)
    
    print(f"\nModel saved to: {MODEL_DIR}/price_lstm_{crop_name.lower()}.h5")
    
    return model, scaler, history

def predict_future_prices(model, scaler, last_sequence, days=30):
    """Predict future prices"""
    predictions = []
    current_seq = last_sequence.copy()
    
    for _ in range(days):
        # Predict next value
        pred = model.predict(current_seq.reshape(1, -1, 1), verbose=0)
        predictions.append(pred[0, 0])
        
        # Update sequence
        current_seq = np.roll(current_seq, -1)
        current_seq[-1] = pred[0, 0]
    
    # Inverse transform
    predictions = np.array(predictions).reshape(-1, 1)
    predictions = scaler.inverse_transform(predictions)
    
    return predictions.flatten()

def train_all_crops():
    """Train models for all crops"""
    crops = ["Rice", "Wheat", "Maize", "Soybean", "Cotton", "Sugarcane"]
    
    for crop in crops:
        try:
            train_price_model(crop, seq_length=60, epochs=30)
        except Exception as e:
            print(f"Error training {crop}: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("LSTM Price Prediction Model Training")
    print("=" * 60)
    
    # Check if data exists
    data_file = os.path.join(DATA_DIR, "crop_prices.csv")
    if not os.path.exists(data_file):
        print(f"Data file not found: {data_file}")
        print("Please run generate_sample_data.py first.")
        exit(1)
    
    # Train for all crops
    if TF_AVAILABLE:
        train_all_crops()
        
        print("\n" + "=" * 60)
        print("Training for all crops completed!")
        print("=" * 60)
    else:
        print("\nTo train models, install TensorFlow:")
        print("pip install tensorflow")
