import requests
from cookies_and_headers import cookies, headers
import os
import pandas as pd

# Create folder to get and store data
path_Data_Folder = './CrawlData/Data_File/'
os.makedirs(path_Data_Folder, exist_ok=True)

url='https://tiki.vn/api/v2/reviews'
max_items = 20

params = {
    'limit': str(max_items),
    'include': 'comments,contribute_info,attribute_vote_summary',
    'sort': 'score|desc,id|desc,stars|all',
    'page': '1',
    'spid': '10853528',
    'product_id': '3304875',
}

# Read Product_IDs from CSV File
product_ids = pd.read_csv('./CrawlData/CSVFile/URLKeys.csv')

def extract_review(category: str, product_id : int, page_review : int, create_folder = True):
    '''
    Extract review from a page in category folder
        Data folder + {category} + Reviews + review_{product_id}_page_{page}.json
    Objective: Extract review from product_id and save as json file
    '''
    if create_folder:
        os.makedirs(path_Data_Folder + str(category) + '/Reviews/review_' + str(product_id), exist_ok=True)
    path_json_file = path_Data_Folder + str(category) + '/Reviews/review_' + str(product_id) + '/page_' + str(page_review) + '.json'

    # If json does not exist, return
    if os.path.exists(path_json_file):
        return False

    # Get review
    params['product_id'] = str(product_id)
    params['page'] = str(page_review)
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    response.raise_for_status()

    # Save data to json file
    data = response.json()
    if created_folder:
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
    for _, row in product_ids.iterrows():
        category = row['URLKeys']
        path_product = path_Data_Folder + str(category) + '/page_'
        for page_product in range(1, 10):
            path_json_file = path_product + str(page_product) + '.json'
            if not os.path.exists(path_json_file):
                break
            df = pd.read_json(path_json_file)
            product_ids = df['id']
            for product_id in product_ids:
                created_folder = True
                for page_review in range(1, 10):
                    if not extract_review(category, product_id, page_review, created_folder):
                        break
                    created_folder = False
except Exception as e:
    print('Error: ', e)
