import pandas as pd
import re
from unidecode import unidecode

def clean_text(text):
    text = unidecode(text)  
    text = re.sub(r'\s+', ' ', text)  
    text = re.sub(r'[^a-zA-Z0-9\s.,!?&%$-]', '', text)  
    return text

def load_and_clean_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8', low_memory=False)
    except Exception as e:
        raise ValueError(f"Error loading file: {e}")

    required_columns = ['Product ID', 'Product Name', 'Category', 'Price (USD)', 'Stock Status', 'Return Policy', 'Customer Support Info']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"CSV file is missing required columns: {missing_columns}")

    df.drop_duplicates(inplace=True)

  
    df['Product ID'] = df['Product ID'].fillna('N/A').astype(str)
    df['Product Name'] = df['Product Name'].fillna('Unnamed Product')
    df['Category'] = df['Category'].fillna('General')
    df['Price (USD)'] = pd.to_numeric(df['Price (USD)'], errors='coerce').fillna(0.0)
    df['Stock Status'] = df['Stock Status'].fillna('N/A')
    df['Return Policy'] = df['Return Policy'].fillna('No return policy available')
    df['Customer Support Info'] = df['Customer Support Info'].fillna('No customer support information available')

   
    for col in ['Product Name', 'Category', 'Stock Status', 'Return Policy', 'Customer Support Info']:
        df[col] = df[col].apply(clean_text)

    
    if df.empty:
        raise ValueError("The dataset is empty after cleaning.")

    return df
