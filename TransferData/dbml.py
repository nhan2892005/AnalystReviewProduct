import re

dbml_content = '''
Table dim_Product {
  product_id INT [pk]
  name STRING
  description STRING
  category_id INT 
  brand_id INT
  sellerId INT
  price MONEY
  discount INT
  rating_average FLOAT
  review_count INT
  star JSON
  updated_date_id INT
}

Table dim_Customer {
  customer_id INT pk
  name STRING
  full_name STRING
  region STRING
  created_time TIMESTAMP
  total_reviews INT
  total_thanks INT
}

Table dim_Seller {
  seller_id INT [pk]
  name STRING
  is_best_store BOOLEAN
}

Table dim_Category {
  category_id INT [pk]
  name STRING
}

Table dim_Brand {
  brand_id int [pk]
  name VARCHAR(255)
}

Table dim_Date {
  date_id INT [pk]
  date INT
  day INT
  month INT
  year INT
  quarter INT
  is_weekend BOOLEAN
  is_holiday BOOLEAN
}

Table fact_Comment{
  comment_id INT [pk]
  review_id INT 
  commentator STRING
  customer_id INT 
  content STRING
  score FLOAT
  is_reported BOOLEAN
}

Table fact_Sales{
  sale_id INT [pk]
  product_id INT 
  customer_id INT 
  seller_id INT 
  date_id INT 
  quantity INT
  price FLOAT
  discount INT
  total_amount INT
}

Table fact_Reviews{
  review_id INT [pk]
  product_id INT 
  customer_id INT 
  seller_id INT
  title STRING
  date_id INT
  delivery_date INT
  title STRING
  comment_count INT
  rating FLOAT
  content STRING
  thank_count INT
}
'''

def get_table_definitions():
    table_definitions = re.findall(r'Table\s+\w+\s*{[^}]+}', dbml_content, re.DOTALL)
    return table_definitions
