import pdfplumber
import pandas as pd
import re
import sys

def special_case_for_header(header):
    if header == 'Công ty':
        return "Company"
    # elif header == "Tổng số ngày nghỉ hưởng lương BHXH (tỷ lệ 75%)":
    #     return "Leave days subject to 75% Social Insurance"
    # elif header == "Tổng số ngày nghỉ hưởng lương BHXH (tỷ lệ 100%)":
    #     return "Leave days subject to 100% Social Insurance"
    elif header == "Lương doanh số Commission":
        return "Comission"
    else:
        return header

# Define the function to extract tables from the PDF
def clean_headers(headers):
    """Clean column headers by removing Vietnamese words and replacing spaces with underscores."""
    cleaned = []
    for header in headers:
        # Remove Vietnamese words (containing diacritics) and keep only English words
        try:
            english_only = header.split("/ ")[1]
        except IndexError as e:
            # print(header)
            english_only = header
        cleaned.append(special_case_for_header(english_only).strip().replace(' ', '_'))  # Replace spaces with underscores
    return cleaned

def extract_cleaned_tables_with_index(pdf_path):
    """Extract tables, clean headers, remove Vietnamese words, and add an index column."""
    with pdfplumber.open(pdf_path) as pdf:
        tables = []
        for page in pdf.pages:
            page_tables = page.extract_tables()
            for table in page_tables:
                if table:  # Ensure the table is not empty
                    df = pd.DataFrame(table[1:], columns=table[0]).transpose()
                    df.reset_index(inplace=True)
                    df.columns = clean_headers(df.iloc[0])  # Clean headers
                    df = df.drop(df.index[0])  # Drop the row used for column names
                    tables.append(df)
    return tables


# Path to the uploaded PDF file
pdf_path = r"D:\Hungtv7\Personal_Fin\VNG_payslip\payslip_VG-15316_2021_04.pdf"

# Extract tables from the PDF file
tables = extract_cleaned_tables_with_index(pdf_path)

# Display the first few rows of each extracted table for illustration
for i, table in enumerate(tables):
    if table.shape[0] < 3:
        table.drop([1])   
    elif table.shape[0] >= 3:
        table.drop([1])
    print(f"Transposed Table {i+1}:\n", table)
