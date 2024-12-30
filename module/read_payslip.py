import pdfplumber
import pandas as pd
import json
import re
import os
import sys

class pdfReader():
    def __init__(self, pdf_path, path_column_schema=None):
        self.__pdf_path = pdf_path
        self.__path_col_schema  = path_column_schema

    @property
    def path_col_schema(self):
        return self.__path_col_schema
    @path_col_schema.setter
    def path_col_schema(self, path_col_schema):
        if os.path.exists(path_col_schema):
            self.__path_col_schema = path_col_schema
        else:
            raise FileNotFoundError(f"File not found: {path_col_schema}")
        
    def extract_tables(self):
        """Extract tables from the PDF file."""
        with pdfplumber.open(self.__pdf_path) as pdf:
            tables = []
            for page in pdf.pages:
                page_tables = page.extract_tables()
                for table in page_tables:
                    if table:
                        tables.append(pd.DataFrame(table))
        return tables

    def clean_headers(self, headers):
        """Clean column headers by removing Vietnamese words stand before slash and replacing spaces with underscores."""
        cleaned = []
        for header in headers:
            # Remove Vietnamese words (containing diacritics) and keep only English words

            for char in ("/", "\n"):
                try:
                    english_only = header.split(char)[1]
                except IndexError as e:
                    continue
                else:
                    english_only = header

            cleaned.append(english_only.strip().replace(' ', '_'))  # Replace spaces with underscores
        return cleaned
    
    def exportColName(self, tables):
        """"Export list col names from dataframe to json file to prepare for mapping"""
        # tables = self.extract_tables()
        final_dict = {}
        for i, table in enumerate(tables):
            if i == 0:
                continue
            # Assuming target headers are column's names
            headers = table.columns.tolist()

            # Create a dict with column's names as keys and empty string as values
            col_dict = {header: "" for header in headers}
            final_dict.update(col_dict)
            # Export the dict to  a JSON file
        with open(self.__path_col_schema, "w") as f:
            json.dump(final_dict, f, indent=4)
        



class payslipReader(pdfReader):
    def __init__(self, pdf_path, path_column_schema=r"D:\\Hungtv7\\Personal_Fin\\config\\VNG_payslip.json"):
        super().__init__(pdf_path, path_column_schema)

    def special_case_for_header(header):
        # List of special cases for column names
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
    
    def clean_headers(self, headers):
        """Clean column headers by removing Vietnamese words stand before slash and replacing spaces with underscores."""
        cleaned = []
        for header in headers:
            # Remove Vietnamese words (containing diacritics) and keep only English words
            
            for char in ("/", "\n"):
                try:
                    english_only = payslipReader.special_case_for_header(header.split(f"{char}")[1])
                except IndexError as e:
                    continue
                    
            # print(english_only.strip().replace(' ', '_'))
            cleaned.append(english_only.strip().replace(' ', '_'))  # Replace spaces with underscores
        return cleaned
        
    def extract_tables(self):
        """Extract tables from the PDF file."""
        with pdfplumber.open(self._pdfReader__pdf_path) as pdf:
            tables = []
            for page in pdf.pages:
                page_tables = page.extract_tables()
                for table in page_tables:
                    if table:
                        # Transpose the table to have columns as headers
                        df = pd.DataFrame(table[1:], columns=table[0]).transpose()
                        df.reset_index(inplace=True)
                        df.columns = self.clean_headers(df.iloc[0])  # Clean headers
                        df = df.drop(df.index[0])  # Drop the row used for column names
                        tables.append(df)
        return tables
    
    def clean_tables(self):
        """Clean the table by removing rows with all NaN and No meaning values."""
        transposed_tables = self.extract_tables()
        cleaned_tables = []
        general_info = transposed_tables[0]
        salary_info = transposed_tables[1]
        working_info = transposed_tables[2]
        derived_detail = transposed_tables[4]
        bonus_detail = transposed_tables[5]
        deduction_info = transposed_tables[7]
        deduction_detail = transposed_tables[8]
        net_income = transposed_tables[9]

        # Remove 3 rows from table
        salary_info = salary_info.drop(salary_info.index[0:3])
        working_info = working_info.drop(working_info.index[0:3])
        derived_detail = derived_detail.drop(derived_detail.index[0:3])
        # Add distinct tables to the list
        cleaned_tables.append(general_info)
        cleaned_tables.append(salary_info)
        cleaned_tables.append(working_info)
        cleaned_tables.append(derived_detail)

        # Remove 2 rows from table
        bonus_detail = bonus_detail.drop(bonus_detail.index[0:2])
        deduction_detail = deduction_detail.drop(deduction_detail.index[0:2])
        net_income = net_income.drop(net_income.index[0:2])
        # Add distinct tables to the list
        cleaned_tables.append(bonus_detail)
        cleaned_tables.append(deduction_info)
        cleaned_tables.append(deduction_detail)
        cleaned_tables.append(net_income)

        # Return list of tables removed all unnecessary rows
        return cleaned_tables

vng_payslip_reader = payslipReader(r"D:\Hungtv7\Personal_Fin\VNG_payslip\payslip_VG-15316_2021_04.pdf")

# tables = vng_payslip_reader.extract_tables() # Extract tables from the PDF file
transposed_tables = vng_payslip_reader.clean_tables() # Clean the tables
vng_payslip_reader.exportColName(transposed_tables) # Export column names to a JSON file
