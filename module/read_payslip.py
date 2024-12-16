import pdfplumber
import pandas as pd

# Define the function to extract tables from the PDF
def extract_tables_with_transpose(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        tables = []
        for page in pdf.pages:
            page_tables = page.extract_tables()
            for table in page_tables:
                # Convert the table to a DataFrame and transpose it
                df = pd.DataFrame(table[1:], columns=table[0]).transpose()
                df.columns = df.iloc[0]  # Set the first row as column headers
                df = df.drop(df.index[0])  # Drop the first row after setting it as header
                tables.append(df)
    return tables


# Path to the uploaded PDF file
pdf_path = r"D:\Hungtv7\Personal_Fin\payslip_VG-15316.pdf"

# Extract tables from the PDF file
tables = extract_tables_with_transpose(pdf_path)

# Display the first few rows of each extracted table for illustration
for i, table in enumerate(tables):
    print(f"Transposed Table {i+1}:\n", table)