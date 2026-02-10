import pandas as pd
import os

def extract_gpu(text):
    if not isinstance(text, str):
        return "Internal/Other"
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

def process_v2():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, 'data', 'laptops_cleaned_v2.csv')
    output_path = os.path.join(base_dir, 'data', 'laptops_v2_ready.csv')
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    print(f"Reading {input_path}...")
    df = pd.read_csv(input_path)
    
    print("Extracting GPU...")
    df['GPU'] = df['Combined_Text'].apply(extract_gpu)
    
    print(f"Saving to {output_path}...")
    df.to_csv(output_path, index=False)
    print("Done.")

if __name__ == "__main__":
    process_v2()
