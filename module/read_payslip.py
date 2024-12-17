import pdfplumber
import pandas as pd
import sys
import re

# Define the function to extract tables from the PDF
def clean_headers(headers):
    """Clean column headers: remove Vietnamese, keep English, and replace spaces with underscores."""
    cleaned = []
    for header in headers:
        # Remove Vietnamese and keep only English words
        english_only = re.sub(r'[^\x00-\x7F]+', '', header)  # Remove non-ASCII characters
        english_only = re.sub(r'[^a-zA-Z0-9 ]', '', english_only)  # Remove special characters
        cleaned.append(english_only.strip().replace(' ', '_'))
    return cleaned

def extract_cleaned_tables(pdf_path):
    """Extract tables from PDF, clean headers, and transpose rows into columns."""
    with pdfplumber.open(pdf_path) as pdf:
        tables = []
        for page in pdf.pages:
            page_tables = page.extract_tables()
            for table in page_tables:
                if table:  # Ensure the table is not empty
                    df = pd.DataFrame(table[1:], columns=table[0]).transpose()
                    df.columns = clean_headers(df.iloc[0])  # Clean headers
                    print(df)
                    df = df.drop(df.index[0])  # Drop the header row used for columns
                    df.insert(0, "Index", range(1, len(df) + 1))
                    print(df)
                    tables.append(df)
    return tables

def split_column_header_vi_en(col_header):
    # print("Cols name: ", col_header)
    if col_header == 'idx':
        return col_header
    try:
        # print("Cols name processed: ", col_header.split('/ ')[1])
        return col_header.split('/ ')[1].strip().replace(' ', '_')
    except Exception as e:
        try:
            # print("Cols name processed: ", col_header.split('\n')[1])
            return col_header.split('\n')[1].strip()
        except Exception as e:
            # print("Cols name processed: ", col_header.split(' ')[1])
            return col_header.split(' ')[1].strip()
    

def insert_into_pg():
    # Your code here
    pass

if __name__ ==  '__main__':
    # Path to the uploaded PDF file
    pdf_path = r"D:\Hungtv7\Personal_Fin\VNG_payslip\payslip_VG-15316_2021_04.pdf"

    # Extract tables from the PDF file
    tables = extract_cleaned_tables(pdf_path)
    
    # Display the first few rows of each extracted table for illustration
    # for i, table in enumerate(tables):
    #     print(f"Transposed Table {i+1}:\n", table)