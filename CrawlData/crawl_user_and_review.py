import requests
from cookies_and_headers import cookies, headers
import os
import pandas as pd

# Create folder to store crawled data
path_Data_Folder = './CrawlData/Data_File/'
os.makedirs(path_Data_Folder, exist_ok=True)

# API endpoint for fetching reviews
url = 'https://tiki.vn/api/v2/reviews'
max_items = 20

# Parameters for the API request
params = {
    'limit': str(max_items),
    'include': 'comments,contribute_info,attribute_vote_summary',
    'sort': 'score|desc,id|desc,stars|all',
    'page': '1',
    'spid': '10853528',
    'product_id': '3304875',
}

# Read Product IDs from CSV File
product_ids = pd.read_csv('./CrawlData/CSVFile/URLKeys.csv')

def extract_review(category: str, product_id: int, page_review: int, create_folder = True):
    '''
    Extract reviews for a product and save as JSON file
    
    Args:
        category (str): Product category
        product_id (int): ID of the product
        page_review (int): Page number of reviews
        create_folder (bool): Whether to create a new folder for the product
    
    Returns:
        bool: True if new data was extracted, False if file already exists
    '''
    # Create folder structure for storing reviews
    if create_folder:
        os.makedirs(path_Data_Folder + str(category) + '/Reviews/review_' + str(product_id), exist_ok=True)
    path_json_file = path_Data_Folder + str(category) + '/Reviews/review_' + str(product_id) + '/page_' + str(page_review) + '.json'

    # Check if file already exists
    if os.path.exists(path_json_file):
        print(f'File already exists: {path_json_file}')
        return False

    # Fetch review data from API
    params['product_id'] = str(product_id)
    params['page'] = str(page_review)
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    response.raise_for_status()

    # Save review data to JSON file
    data = response.json()
    if create_folder:
        # Save overview data for the first page
        overview_data_review = {
            'stars': data['stars'],
            'reviews_count': data['reviews_count'],
        }
        df_overview = pd.DataFrame([overview_data_review])
        df_overview.to_json(path_Data_Folder + str(category) + '/Reviews/review_' + str(product_id) + '/overview.json', indent=2)
    
    df_review = pd.DataFrame(data['data'])
    df_review.to_json(path_json_file, indent=2)
    return True

try:
    # Iterate through product categories
    for _, row in product_ids.iloc[7:10].iterrows():
        category = row['URLKeys']
        path_product = path_Data_Folder + str(category) + '/page_'
        
        # Iterate through product pages
        for page_product in range(1, 10): # Notes: from dien_gia_dung, crawl only 5 page
            path_json_file = path_product + str(page_product) + '.json'
            if not os.path.exists(path_json_file):
                break
            
            # Read product IDs from JSON file
            df = pd.read_json(path_json_file)
            product_ids = df['id']
            print(f'Crawling {row}')
            
            # Extract reviews for each product
            for product_id in product_ids:
                created_folder = True
                for page_review in range(6, 10): # Notes: from dien_gia_dung, crawl 5 page, next, crawl 6 -> 10
                    if not extract_review(category, product_id, page_review, created_folder):
                        break
                    created_folder = False
except Exception as e:
    print('Error: ', e)
