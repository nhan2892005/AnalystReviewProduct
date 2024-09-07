import requests
from cookies_and_headers import cookies, headers
import os
import pandas as pd

# !Objective: crawl Product data 
# Store in ./CrawlData/Data_File/{category}/Products/p{product_id}.json

# Create folder to store crawled data
path_Data_Folder = './CrawlData/Data_File/'
os.makedirs(path_Data_Folder, exist_ok=True)

def extract_product(category : str, page : int, url, params):
    '''
    Extract product details from a specific page in a category
    Args:
        category (str): The category of products
        page (int): The page number to extract from
    Returns:
        bool: True if extraction was successful, False otherwise
    '''
    
    # Create directory for the category's products
    os.makedirs(path_Data_Folder + str(category) + '/Products', exist_ok=True)
    path_json_file = path_Data_Folder + str(category) + '/page_' + str(page) + '.json'

    # Check if the JSON file for this page exists
    if not os.path.exists(path_json_file):
        return False

    # Read product IDs from the JSON file
    df = pd.read_json(path_json_file)
    product_ids = df['id']

    for product_id in product_ids:
        path_Product = path_Data_Folder + str(category) + '/Products/p' + str(product_id) + '.json'
        # Skip if product data already exists
        if os.path.exists(path_Product):
            print('Product {} already exists'.format(product_id))
            continue
        # Fetch product details from API
        response = requests.get(url.format(product_id), headers=headers, cookies=cookies, params=params)
        response.raise_for_status()

        # Save product data to JSON file
        data = response.json()
        df_product = pd.DataFrame([data])
        df_product.to_json(path_Product, indent=2)
    return True

def crawl_Products_data(start_category: str = None, start_page: int = None, end_page: int = None):
    '''
    Objective: Crawl product data from categories and pages
    '''
    # API endpoint for product details
    url='https://tiki.vn/api/v2/products/{}'

    # Parameters for API request
    params = {
        'platform' : 'web',
        'spid' : '10853528',
        'version' : '3',
    }

    # Read Product IDs from CSV File
    product_ids = pd.read_csv('./CrawlData/CSVFile/URLKeys.csv')

    if start_category and start_category not in product_ids['URLKeys'].values:
        print('Invalid category. Choose from: ', product_ids['URLKeys'].values)
        return
    
    try:
        # Iterate through all categories and pages
        for _, row in product_ids.iterrows():
            category = row['URLKeys']
            if start_category and category != start_category:
                continue
            print('Processing: ', category, end=' ')
            for page in range(start_page or 1, end_page or 10): # from page 1 -> page 10 (total: 50 page)
                print(page, end=' ')
                if not extract_product(category, page, url, params):
                    break
            print()
            
    except requests.exceptions.HTTPError as err:
        print('Error: ', err)
        print('Crawl product failed')
        raise