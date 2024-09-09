import os
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv
import json
from lunarcalendar import Converter, Solar, Lunar
from datetime import datetime, timedelta
import numpy as np
from decimal import Decimal

# Set the environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./TransferData/summary-reviews-7e33cf5e1c6f.json"

# Read the environment variable
load_dotenv()
db = os.getenv('db')
dataset = os.getenv('dataset')

# Construct a BigQuery client object.
client = bigquery.Client()

def clean_dataframe(df):
    # Loại bỏ cột price_comparison nếu có
    if 'price_comparison' in df.columns:
        df = df.drop(columns=['price_comparison'])
    
    for column in df.columns:
        if df[column].dtype == 'object':
            # Thay thế chuỗi 'None' bằng None của Python
            df[column] = df[column].replace('None', None)
        
        if column == 'product_id':
            df[column] = pd.to_numeric(df[column], errors='coerce').astype('Int64')
        elif column == 'category_id':
            df[column] = pd.to_numeric(df[column], errors='coerce').astype('Int64')
        elif column == 'brand_id':
            df[column] = pd.to_numeric(df[column], errors='coerce').astype('Int64')
        elif column == 'price':
            df[column] = df[column].astype(float).astype(str).map(lambda x: Decimal(x) if x != 'nan' else None)
        elif column == 'discount':
            df[column] = pd.to_numeric(df[column], errors='coerce').astype('Int64')
        elif column == 'rating_average':
            df[column] = pd.to_numeric(df[column], errors='coerce').astype('float64')
        elif column == 'review_count':
            df[column] = pd.to_numeric(df[column], errors='coerce').astype('Int64')
        elif column == 'star':
            df[column] = df[column].apply(lambda x: json.dumps(x) if pd.notnull(x) else None)
        elif column == 'updated_date_id':
            df[column] = pd.to_numeric(df[column], errors='coerce').astype('Int64')
    
    # In ra thông tin về các cột và kiểu dữ liệu
    print(df.dtypes)
    print(df.head())
    
    return df

def insert_data_to_bigquery(table_id, df):
    # Làm sạch DataFrame trước khi insert
    df = clean_dataframe(df)
    
    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        schema_update_options=[
            bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION,
            bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION,
        ],
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND
    )
    
    job = client.load_table_from_dataframe(
        df, table_id, job_config=job_config
    )
    
    job.result()  # Wait for the job to complete
    
    print(f"Đã chèn {len(df)} dòng vào {table_id}")

# Khởi tạo các DataFrame toàn cục
df_products = None
df_categories = None
df_brands = None
df_sellers = None

def process_products(file_path):
    global df_products
    df = pd.read_json(file_path)
    df = df.rename(columns={
        "id": "product_id",
        "categoryId": "category_id",
        "brandId": "brand_id"
    })
    
    if 'stars' in df.columns:
        df["stars"] = df["stars"].apply(lambda x: json.dumps(x) if pd.notnull(x) else None)
    else:
        print(f"Cột 'stars' không tồn tại trong file {file_path}")
        df["stars"] = None
    
    df["updated_date_id"] = pd.to_datetime("today").strftime("%Y%m%d")
    
    if df_products is None:
        df_products = df
    else:
        df_products = pd.concat([df_products, df], ignore_index=True)

    print(f"Đã xử lý {len(df)} sản phẩm từ {file_path}")

def process_categories(file_path):
    global df_categories
    df = pd.read_json(file_path)
    
    if df_categories is None:
        df_categories = df
    else:
        df_categories = pd.concat([df_categories, df], ignore_index=True)
    
    print(f"Đã xử lý {len(df)} danh mục từ {file_path}")

def process_brands(file_path):
    global df_brands
    df = pd.read_json(file_path)
    df = df.rename(columns={"id": "brand_id"})
    df['name'] = df['name'].astype(str)  # Đảm bảo kiểu dữ liệu là string
    
    if df_brands is None:
        df_brands = df
    else:
        df_brands = pd.concat([df_brands, df], ignore_index=True)
    
    print(f"Đã xử lý {len(df)} thương hiệu từ {file_path}")

def process_sellers(file_path):
    global df_sellers
    df = pd.read_json(file_path)
    df = df.rename(columns={"id": "seller_id"})
    df['name'] = df['name'].astype(str)  # Đảm bảo kiểu dữ liệu là string
    
    if df_sellers is None:
        df_sellers = df
    else:
        df_sellers = pd.concat([df_sellers, df], ignore_index=True)
    
    print(f"Đã xử lý {len(df)} người bán từ {file_path}")

def createDate():
    # From 2000-01-01 to 2030-12-31
    date = pd.date_range(start="2000-01-01", end="2030-12-31")
    df = pd.DataFrame(date, columns=["date"])
    df["date_id"] = df["date"].dt.strftime("%Y%m%d").astype(int)
    df["day"] = df["date"].dt.day
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["quarter"] = df["date"].dt.quarter
    df["is_weekend"] = df["date"].dt.dayofweek >= 5
    df["is_holiday"] = False
    # holiday
    for year in range(2000, 2031):
        tet = Converter.Lunar2Solar(Lunar(year, 1, 1))
        tet_date = datetime(tet.year, tet.month, tet.day)
        start_tet = tet_date - timedelta(days=4)  # 28 tháng Chạp
        end_tet = tet_date + timedelta(days=9)    # Mùng 10 tháng Giêng
        
        mask = (df['date'] >= start_tet) & (df['date'] <= end_tet)
        df.loc[mask, 'is_holiday'] = True

    df.loc[df["date"].dt.month == 1, "is_holiday"] |= df["date"].dt.day == 1
    df.loc[df["date"].dt.month == 3, "is_holiday"] |= df["date"].dt.day == 8
    df.loc[df["date"].dt.month == 4, "is_holiday"] |= df["date"].dt.day == 30
    df.loc[df["date"].dt.month == 5, "is_holiday"] |= df["date"].dt.day == 1
    df.loc[df["date"].dt.month == 9, "is_holiday"] |= (df["date"].dt.day == 2) | (df["date"].dt.day == 3)
    df.loc[df["date"].dt.month == 10, "is_holiday"] |= df["date"].dt.day == 20
    df.loc[df["date"].dt.month == 11, "is_holiday"] |= df["date"].dt.day == 20
    
    print(df[df["date"] == "2024-10-20"])
    insert_data_to_bigquery(f"{db}.{dataset}.dim_Date", df)

def get_Product_dataFrame(urlKeys):
    for urlKey in urlKeys:
        file_path_product = f"./Records/{urlKey}/products.json"
        
        process_products(file_path_product)
        
    return df_products

def get_Categories_dataFrame(urlKeys):
    for urlKey in urlKeys:
        file_path_categories = f"./Records/{urlKey}/categories.json"
        
        process_categories(file_path_categories)
        
    return df_categories

def get_Brands_dataFrame(urlKeys):
    for urlKey in urlKeys:
        file_path_brands = f"./Records/{urlKey}/brands.json"
        
        process_categories(file_path_brands)
        
    return df_brands

def get_Sellers_dataFrame(urlKeys):
    for urlKey in urlKeys:
        file_path_sellers = f"./Records/{urlKey}/sellers.json"
        
        process_categories(file_path_sellers)
        
    return df_sellers

# Hàm để xử lý tất cả các file
def process_all_files(urlKeys):
    for urlKey in urlKeys:
        file_path_product = f"./Records/{urlKey}/products.json"
        file_path_category = f"./Records/{urlKey}/categories.json"
        file_path_brand = f"./Records/{urlKey}/brands.json"
        file_path_seller = f"./Records/{urlKey}/sellers.json"
        
        process_products(file_path_product)
        process_categories(file_path_category)
        process_brands(file_path_brand)
        process_sellers(file_path_seller)

# Hàm để loại bỏ các dòng trùng lặp và in thống kê
def remove_duplicates_and_print_stats():
    global df_products, df_categories, df_brands, df_sellers
    
    if df_products is not None:
        df_products = df_products.drop_duplicates(subset=['product_id'], keep='first')
        print(f"Tổng số sản phẩm sau khi loại bỏ trùng lặp: {len(df_products)}")
    
    if df_categories is not None:
        df_categories = df_categories.drop_duplicates(subset=['id'], keep='first')
        print(f"Tổng số danh mục sau khi loại bỏ trùng lặp: {len(df_categories)}")
    
    if df_brands is not None:
        df_brands = df_brands.drop_duplicates(subset=['brand_id'], keep='first')
        print(f"Tổng số thương hiệu sau khi loại bỏ trùng lặp: {len(df_brands)}")
    
    if df_sellers is not None:
        df_sellers = df_sellers.drop_duplicates(subset=['seller_id'], keep='first')
        print(f"Tổng số người bán sau khi loại bỏ trùng lặp: {len(df_sellers)}")

# Hàm chính để chạy toàn bộ quá trình
def main():
    product_categories_urlKey = pd.read_csv('./CrawlData/CSVFile/URLKeys.csv')
    product_categories_urlKey = product_categories_urlKey['URLKeys'].tolist()

    process_all_files(product_categories_urlKey)  # Xử lý 2 URLKeys đầu tiên
    remove_duplicates_and_print_stats()

    # Insert data into BigQuery
    if df_products is not None:
        # Sắp xếp df_products theo yêu cầu
        df_products_sorted = df_products.sort_values(
            by=['category_id', 'rating_average', 'updated_date_id', 'price'],
            ascending=[True, False, False, True]
        )
        insert_data_to_bigquery(f"{db}.{dataset}.dim_Product", df_products_sorted)
'''
    if df_categories is not None:
        insert_data_to_bigquery(f"{db}.{dataset}.dim_Category", df_categories)

    if df_brands is not None:
        insert_data_to_bigquery(f"{db}.{dataset}.dim_Brand", df_brands)

    if df_sellers is not None:
        insert_data_to_bigquery(f"{db}.{dataset}.dim_Seller", df_sellers)
'''

if __name__ == "__main__":
    main()

