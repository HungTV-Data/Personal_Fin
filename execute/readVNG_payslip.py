import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from module.read_payslip import payslipReader



if __name__ == "__main__":
    # Define the folder path
    folder_path = './VNG_payslip/payslip_VG-15316_2023_05.pdf'

    vng_payslip_reader = payslipReader(folder_path)
    # tables = vng_payslip_reader.extract_tables() # Extract tables from the PDF file
    transposed_tables = vng_payslip_reader.clean_tables() # Clean the tables
    for i, table in enumerate(transposed_tables):
        print(f"Table {i + 1}")
        print(table)
        print("\n")