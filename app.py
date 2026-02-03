import streamlit as st
import joblib
import pandas as pd
import os

# Set page config
st.set_page_config(
    page_title="Laptop Price Predictor",
    page_icon="💻",
    layout="centered"
)

# Load Model
@st.cache_resource
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'laptop_price_model.joblib')
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        return None

model = load_model()

# Title and Description
st.title("💻 Laptop Price Predictor")
st.write("Enter the laptop specifications below to get an estimated price.")

if model is None:
    st.error("Model not found! Please run `train_models.py` first.")
else:
    # Input Form
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            brand = st.selectbox("Brand", ["HP", "Dell", "Lenovo", "Asus", "Acer", "MSI", "Apple", "Samsung", "Other"])
            ram = st.number_input("RAM (GB)", min_value=4, max_value=64, value=8, step=4)
            storage = st.number_input("Storage (GB)", min_value=128, max_value=4096, value=512, step=128)
            
        with col2:
            processor = st.selectbox("Processor", [
                "Intel Core i3", "Intel Core i5", "Intel Core i7", "Intel Core i9",
                "AMD Ryzen 3", "AMD Ryzen 5", "AMD Ryzen 7", "AMD Ryzen 9",
                "Apple M1", "Apple M2", "Apple M3",
                "Intel Celeron", "Intel Pentium", "Other"
            ])
            gpu = st.selectbox("GPU", [
                "Integrated/Other", "Intel Iris Xe", "Intel UHD", "AMD Radeon",
                "NVIDIA RTX 3050", "NVIDIA RTX 4050", "NVIDIA RTX 4060",
                "NVIDIA GTX 1650", "NVIDIA RTX 3060", "NVIDIA RTX 4070",
                "Apple Silicon GPU", "Intel Arc"
            ])
            display = st.number_input("Display Size (Inch)", min_value=10.0, max_value=21.0, value=15.6, step=0.1)
            
        submitted = st.form_submit_button("Predict Price")
        
        if submitted:
            # Create DataFrame for prediction
            input_data = pd.DataFrame({
                'Brand': [brand],
                'RAM': [ram],
                'Storage_GB': [storage],
                'Processor': [processor],
                'GPU': [gpu],
                'Display_Inch': [display]
            })
            
            # Predict
            try:
                prediction = model.predict(input_data)[0]
                st.success(f"Estimated Price: ₹{prediction:,.2f}")
            except Exception as e:
                st.error(f"Error during prediction: {e}")

st.markdown("---")
st.caption("Built with Streamlit and Scikit-Learn")
