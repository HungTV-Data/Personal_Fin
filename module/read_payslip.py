import pdfplumber
import pandas as pd

# Define the function to extract tables from the PDF
def clean_headers(headers):
    """Clean column headers by removing Vietnamese words and replacing spaces with underscores."""
    cleaned = []
    for header in headers:
        # Remove Vietnamese words (containing diacritics) and keep only English words
        english_only = ' '.join(re.findall(r'\b[a-zA-Z0-9]+\b', header))  # Keep only words with a-z, A-Z, 0-9
        cleaned.append(english_only.strip().replace(' ', '_'))  # Replace spaces with underscores
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
                    df.columns = clean_headers(df.iloc[0])  # Clean headers
                    df = df.drop(df.index[0])  # Drop the row used for column names
                    df.insert(0, "Index", range(1, len(df) + 1))  # Add an index column
                    tables.append(df)
    return tables


# Path to the uploaded PDF file
pdf_path = r"D:\Hungtv7\Personal_Fin\payslip_VG-15316.pdf"

# Extract tables from the PDF file
tables = extract_cleaned_tables_with_index(pdf_path)

# Display the first few rows of each extracted table for illustration
for i, table in enumerate(tables):
    print(f"Transposed Table {i+1}:\n", table)