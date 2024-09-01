import pandas as pd
import os
import re

# Get Path of CSV File
def get_path_csv_file(CSVFile : str):
    return os.path.join(os.path.dirname(__file__), 'CSVFile', CSVFile)

# Read CSV File
def read_csv_file(CSVFile : str):
    return pd.read_csv(get_path_csv_file(CSVFile=CSVFile))

# Remove HTML Tags
def remove_html_tags(text):
    # Define a regular expression pattern to match HTML tags
    clean = re.compile('<.*?>')
    # Substitute the matched tags with an empty string
    return re.sub(clean, '', text)