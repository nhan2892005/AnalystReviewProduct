import pandas as pd
import os

# Get Path of CSV File
def get_path_csv_file(CSVFile : str):
    return os.path.join(os.path.dirname(__file__), 'CSVFile', CSVFile)

# Read CSV File
def read_csv_file(CSVFile : str):
    return pd.read_csv(get_path_csv_file(CSVFile=CSVFile))