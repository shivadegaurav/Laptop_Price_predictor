import joblib
import pandas as pd
import os

def test_model():
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'laptop_price_model.joblib')
    print(f"Loading model from {model_path}...")
    model = joblib.load(model_path)
    print("Model loaded.")
    
    # Test data
    sample_data = pd.DataFrame({
        'Brand': ['HP'],
        'RAM': [8],
        'Storage_GB': [512],
        'Processor': ['Intel Core i5'],
        'GPU': ['Intel Iris Xe'],
        'Display_Inch': [15.6]
    })
    
    print("Predicting for:")
    print(sample_data)
    
    pred = model.predict(sample_data)
    print(f"Prediction: {pred[0]}")

if __name__ == "__main__":
    test_model()
