import os
from module.read_payslip import payslipReader



if __name__ == "__main__":
    # Define the folder path
    folder_path = '/d:/Hungtv7/Personal_Fin/VNG_payslip'

    vng_payslip_reader = payslipReader(folder_path)
