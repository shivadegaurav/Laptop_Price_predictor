import pandas as pd
import re
import os

def extract_ram(text):
    if not isinstance(text, str): return None
    match = re.search(r'(\d+)\s*GB', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

def extract_storage(text):
    if not isinstance(text, str): return 0
    # Search for SSD or HDD
    match = re.search(r'(\d+)\s*(GB|TB)\s*(SSD|HDD)', text, re.IGNORECASE)
    if match:
        val = int(match.group(1))
        unit = match.group(2).upper()
        if unit == 'TB':
            val *= 1024
        return val
    return 0

def extract_processor(text):
    if not isinstance(text, str): return 'Unknown'
    text = text.lower()
    if 'i9' in text: return 'Intel Core i9'
    if 'i7' in text: return 'Intel Core i7'
    if 'i5' in text: return 'Intel Core i5'
    if 'i3' in text: return 'Intel Core i3'
    if 'm1' in text: return 'Apple M1'
    if 'm2' in text: return 'Apple M2'
    if 'm3' in text: return 'Apple M3'
    if 'ryzen 9' in text: return 'AMD Ryzen 9'
    if 'ryzen 7' in text: return 'AMD Ryzen 7'
    if 'ryzen 5' in text: return 'AMD Ryzen 5'
    if 'ryzen 3' in text: return 'AMD Ryzen 3'
    if 'celeron' in text: return 'Intel Celeron'
    if 'pentium' in text: return 'Intel Pentium'
    return 'Other'

def extract_brand(text):
    if not isinstance(text, str): return 'Other'
    return text.split()[0].title()

def extract_display(text):
    if not isinstance(text, str): return None
    match = re.search(r'(\d+(\.\d+)?)\s*(Inch|cm|inch)', text, re.IGNORECASE)
    if match:
        val = float(match.group(1))
        if 'cm' in match.group(3).lower():
            val = val / 2.54 # Convert cm to inch
        return round(val, 1)
    return None

def clean_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    
    # Load files
    amazon_file = os.path.join(data_dir, 'amazon_laptops.csv')
    flipkart_file = os.path.join(data_dir, 'flipkart_laptops.csv')
    
    df_amazon = pd.read_csv(amazon_file) if os.path.exists(amazon_file) else pd.DataFrame()
    df_flipkart = pd.read_csv(flipkart_file) if os.path.exists(flipkart_file) else pd.DataFrame()
    
    print("Amazon Columns:", df_amazon.columns)
    print("Flipkart Columns:", df_flipkart.columns)
    
    # Process Amazon
    if not df_amazon.empty:
        if 'Title' not in df_amazon.columns:
            print("Amazon data missing Title column!")
        else:
            df_amazon['Source'] = 'Amazon'
        # Amazon features are all in Title
        df_amazon['Combined_Text'] = df_amazon['Title'] 
        
    # Process Flipkart
    if not df_flipkart.empty:
        df_flipkart['Source'] = 'Flipkart'
        df_flipkart['Combined_Text'] = df_flipkart['Title'].astype(str) + " " + df_flipkart['Features'].astype(str)
        
    # Combine
    df = pd.concat([df_amazon, df_flipkart], ignore_index=True)
    
    # Feature Engineering
    df['Brand'] = df['Title'].apply(extract_brand)
    df['RAM'] = df['Combined_Text'].apply(extract_ram)
    df['Storage_GB'] = df['Combined_Text'].apply(extract_storage)
    df['Processor'] = df['Combined_Text'].apply(extract_processor)
    
    # Extract GPU
    def extract_gpu(text):
        if not isinstance(text, str):
            return "Other"
        text = text.lower()
        if 'rtx 4090' in text: return 'NVIDIA RTX 4090'
        if 'rtx 4080' in text: return 'NVIDIA RTX 4080'
        if 'rtx 4070' in text: return 'NVIDIA RTX 4070'
        if 'rtx 4060' in text: return 'NVIDIA RTX 4060'
        if 'rtx 4050' in text: return 'NVIDIA RTX 4050'
        if 'rtx 3080' in text: return 'NVIDIA RTX 3080'
        if 'rtx 3070' in text: return 'NVIDIA RTX 3070'
        if 'rtx 3060' in text: return 'NVIDIA RTX 3060'
        if 'rtx 3050' in text: return 'NVIDIA RTX 3050'
        if 'rtx 2050' in text: return 'NVIDIA RTX 2050'
        if 'gtx 1650' in text: return 'NVIDIA GTX 1650'
        if 'intel arc' in text: return 'Intel Arc'
        if 'iris xe' in text or 'intel iris' in text: return 'Intel Iris Xe'
        if 'uhd graphics' in text or 'intel uhd' in text: return 'Intel UHD'
        if 'radeon' in text: return 'AMD Radeon'
        if 'm1' in text or 'm2' in text or 'm3' in text: return 'Apple Silicon GPU'
        return "Integrated/Other"

    df['GPU'] = df['Combined_Text'].apply(extract_gpu)

    df['Display_Inch'] = df['Combined_Text'].apply(extract_display)
    
    # Clean Price
    def clean_price(x):
        if pd.isna(x): return None
        if isinstance(x, (int, float)): return x
        x = str(x).replace('₹', '').replace(',', '').replace('.', '')
        try:
            return float(x)
        except:
            return None
            
    df['Price'] = df['Price'].apply(clean_price)
    
    # Remove rows with empty Price
    df = df.dropna(subset=['Price'])
    
    # Fill missing values
    df['RAM'] = df['RAM'].fillna(df['RAM'].mode()[0])
    df['Storage_GB'] = df['Storage_GB'].fillna(512)
    df['Display_Inch'] = df['Display_Inch'].fillna(15.6)
    
    # Save
    output_path = os.path.join(data_dir, 'cleaned_laptops.csv')
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")
    print(df.head())
    print("\nDataset Info:")
    print(df.info())

if __name__ == "__main__":
    clean_data()
