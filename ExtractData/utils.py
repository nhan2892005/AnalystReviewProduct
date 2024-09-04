import os
import json
import pandas as pd
def store_to_df(df, data):
    '''
    Store data to DataFrame
    Parameters:
        df: DataFrame, data
        data: dict or list, data to be stored
    '''
    try:
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    for k, v in value.items():
                        df.at[0, f'{key}_{k}'] = v
                else:
                    df.at[0, key] = value
        elif isinstance(data, list):
            for i, value in enumerate(data):
                if i < len(df.columns):
                    df.at[0, df.columns[i]] = value
                else:
                    print(f"Warning: More data than columns. Ignoring extra data.")
                    break
        else:
            print(f"Error: Unsupported data type. Expected dict or list, got {type(data)}")
    except Exception as e:
        print(f'Error in store_to_df: {e}')
    return df
def safe_read_json(file_path):
    '''
    Read JSON file if it exists and is not empty, otherwise return an empty DataFrame
    '''
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return pd.DataFrame(data)
                else:
                    return pd.DataFrame([data])
            except json.JSONDecodeError:
                return pd.DataFrame()
    else:
        # Tạo file JSON trống nếu không tồn tại
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump([], f)
        return pd.DataFrame()
    
def add_record(file_name, data, info_num_record=False):
    '''
    Add a record to the Json file
    Parameters:
        file_name: str, name of the file
        data: DataFrame, data to be added
    '''
    if data is None or data.empty:
        return
    # Read existing JSON file
    df = safe_read_json(file_name)

    if info_num_record:
        print(f'Number of records before: {len(df)}')
    
    try:
        # Concatenate and remove duplicates
        if 'id' in df.columns and 'id' in data.columns:
            df = pd.concat([df, data]).drop_duplicates(subset=['id']).reset_index(drop=True)
        else:
            df = pd.concat([df, data]).reset_index(drop=True)

        # Convert DataFrames to dictionaries
        df_dict = df.to_dict(orient='records')

        # Save to JSON
        with open(file_name, 'w') as f:
            json.dump(df_dict, f, indent=2)
    except Exception as e:
        print(f'Error in add_record: {e}')
    finally:
        if info_num_record:
            print(f'Number of records after: {len(df)}')

def get_relate_record(df, name_record, fields):
    '''
    Get related records
    Parameters:
        df: DataFrame, data
        name_record: str, name of the record
        fields: list, fields to be extracted
    '''
    try:
        if name_record in df.columns and isinstance(df[name_record].iloc[0], dict):
            record = pd.DataFrame([{field: df[name_record].iloc[0][field] for field in fields}])
            return record
    except (KeyError, IndexError, TypeError):
        return None