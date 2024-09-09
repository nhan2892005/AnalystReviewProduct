import os
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv

# Thiết lập môi trường
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./TransferData/summary-reviews-7e33cf5e1c6f.json"
db = os.getenv('db')
dataset = os.getenv('dataset')

# Khởi tạo client BigQuery
client = bigquery.Client()

def read_json_to_df(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        df = pd.read_json(file)
    return df

def process_reviews(directory):
    all_reviews = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json') and 'Reviews' in root:
                file_path = os.path.join(root, file)
                df = read_json_to_df(file_path)
                
                # Chuyển đổi và lọc cột theo schema
                df = df.rename(columns={
                    'id': 'review_id',
                    'review_created_date': 'date_id',
                    'delivery_date': 'delivery_date'
                })
                
                df['date_id'] = pd.to_datetime(df['date_id'], format='%Y-%m-%d %H:%M:%S', errors='coerce').dt.strftime('%Y%m%d').fillna('0').astype('int64')

                # Xử lý delivery_date
                df['delivery_date'] = pd.to_datetime(df['delivery_date'], format='%Y-%m-%d %H:%M:%S', errors='coerce').dt.strftime('%Y%m%d').fillna('0').astype('int64')
                
                # Chọn và sắp xếp lại các cột theo schema
                df = df[[
                    'review_id', 'product_id', 'customer_id', 'seller_id',
                    'title', 'date_id', 'delivery_date', 'comment_count',
                    'rating', 'content', 'thank_count'
                ]]
                
                all_reviews.append(df)
    
    if all_reviews:
        return pd.concat(all_reviews, ignore_index=True)
    return pd.DataFrame()

def process_comments(directory):
    all_comments = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json') and 'Comments' in root:
                file_path = os.path.join(root, file)
                df = read_json_to_df(file_path)
                
                # Chọn chỉ các cột cần thiết, không bao gồm 'fullname'
                df = df[[
                    'comment_id', 'review_id', 'commentator', 'customer_id',
                    'content', 'score','is_reported'
                ]]
                all_comments.append(df)
    
    if all_comments:
        return pd.concat(all_comments, ignore_index=True)
    return pd.DataFrame()

def clean_dataframe(df):
    # Xử lý dữ liệu null và kiểu dữ liệu
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('')
        elif df[col].dtype in ['int64', 'float64']:
            df[col] = df[col].fillna(0)
    return df

def insert_data_to_bigquery(table_id, df):
    df = clean_dataframe(df)
    
    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        write_disposition="WRITE_APPEND",
    )
    
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()  # Đợi cho đến khi job hoàn thành
    
    print(f"Loaded {len(df)} rows into {table_id}")
    
def get_Review_df():
    base_directory = 'Records'
    reviews_df = process_reviews(base_directory)
    return reviews_df

def get_Comment_df():
    base_directory = 'Records'
    comments_df = process_comments(base_directory)
    return comments_df

def main():
    base_directory = 'Records'
    
    # Xử lý reviews
    reviews_df = process_reviews(base_directory)
    print(reviews_df['date_id'])
    if not reviews_df.empty:
        reviews_table_id = f"{db}.{dataset}.fact_Reviews"
        insert_data_to_bigquery(reviews_table_id, reviews_df)
    
    # Xử lý comments
    comments_df = process_comments(base_directory)
    print(comments_df.columns)
    print(len(comments_df))
    if not comments_df.empty:
        comments_table_id = f"{db}.{dataset}.fact_Comment"
        insert_data_to_bigquery(comments_table_id, comments_df)

if __name__ == "__main__":
    main()

