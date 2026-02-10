import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

def train_eval():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'laptops_v2_ready.csv')
    
    if not os.path.exists(data_path):
        print("Data file not found!")
        return
        
    df = pd.read_csv(data_path)
    
    # Selected Features
    features = ['Brand', 'RAM', 'Storage_GB', 'Processor', 'GPU', 'Display_Inch']
    target = 'Price'
    
    X = df[features]
    y = df[target]
    
    # Handle missing values in X if any are left (though we filled them in cleaning)
    # Categorical columns
    cat_cols = ['Brand', 'Processor', 'GPU']
    num_cols = ['RAM', 'Storage_GB', 'Display_Inch']
    
    # Preprocessing
    numerical_transformer = SimpleImputer(strategy='mean')
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, num_cols),
            ('cat', categorical_transformer, cat_cols)
        ])
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Models
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42)
    }
    
    results = {}
    
    print("Training Models...\n")
    
    for name, model in models.items():
        # Create pipeline
        clf = Pipeline(steps=[('preprocessor', preprocessor),
                              ('model', model)])
        
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        results[name] = {"MAE": mae, "R2": r2}
        
        print(f"--- {name} ---")
        print(f"MAE: ₹{mae:,.2f}")
        print(f"R2 Score: {r2:.4f}")
        print("-" * 20)
        
    print("\nSummary:")
    print(results)
    
    # Feature Importance for Random Forest
    rf_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                  ('model', models['Random Forest'])])
    rf_pipeline.fit(X, y) # Retrain on full data for final model
    
    # Save Model
    model_path = os.path.join(base_dir, 'models', 'laptop_price_model.joblib')
    joblib.dump(rf_pipeline, model_path)
    print(f"\nModel saved to {model_path}")
    
if __name__ == "__main__":
    train_eval()
