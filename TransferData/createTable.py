import os
from dotenv import load_dotenv
from google.cloud import bigquery
import re
from dbml import get_table_definitions

# Set the environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./TransferData/summary-reviews-7e33cf5e1c6f.json"

# Read the environment variable
load_dotenv()
db = os.getenv('db')
dataset = os.getenv('dataset')

# Construct a BigQuery client object.
client = bigquery.Client()

# Perform a query to create a table
def createTable(TableSchema: dict, tableName: str):
    table_id = f"{db}.{dataset}.{tableName}"
    schema = []
    for key, value in TableSchema.items():
        schema.append(bigquery.SchemaField(key, value))

    table = bigquery.Table(table_id, schema=schema)
    print(table)
    table = client.create_table(table)  # Make an API request.
    print(f"Created table {table_id}")

def create_table_from_definition(table_definition: str):
    # Extract table name and fields
    match = re.match(r'\s*Table\s+(\w+)\s*{\s*([\s\S]+?)\s*}\s*', table_definition, re.DOTALL)
    if not match:
        raise ValueError("Invalid table definition format")
    
    table_name = match.group(1)
    fields_str = match.group(2)

    # Parse fields
    fields = {}
    for line in fields_str.strip().split('\n'):
        # Remove comments and split the line
        line = re.split(r'//|\[', line)[0].strip()
        parts = line.split()
        if len(parts) >= 2:
            field_name = parts[0]
            field_type = parts[1]
            
            # Map SQL types to BigQuery types
            if field_type.upper() == 'INT':
                bq_type = 'INTEGER'
            elif field_type.upper() == 'MONEY':
                bq_type = 'FLOAT'
            elif field_type.upper().startswith('VARCHAR'):
                bq_type = 'STRING'
            else:
                bq_type = field_type.upper()
            
            fields[field_name] = bq_type

    # Create the table
    createTable(fields, table_name)

table_def = get_table_definitions()
for table in table_def[-3:]:
    create_table_from_definition(table)
