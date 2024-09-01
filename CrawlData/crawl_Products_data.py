import requests
from cookies_and_headers import cookies, headers
import os
import pandas as pd

# Create folder to get and store data
path_Data_Folder = './CrawlData/Data_File/'
os.makedirs(path_Data_Folder, exist_ok=True)

url='https://tiki.vn/api/v2/products/{}'

params = {
    'platform' : 'web',
    'spid' : '10853528',
    'version' : '3',
}

# Read Product_IDs from CSV File
product_ids = pd.read_csv('./CrawlData/CSVFile/URLKeys.csv')

def extract_product(category : str, page : int):
    '''
    Extract product from a page in category folder
        Data folder + {category} + page_{page}.json
    Objective: Extract product from product_id and save as json file
    '''
    os.makedirs(path_Data_Folder + str(category) + '/Products', exist_ok=True)
    path_json_file = path_Data_Folder + str(category) + '/page_' + str(page) + '.json'

    # If json does not exist, return
    if not os.path.exists(path_json_file):
        return False

    # Read json file
    df = pd.read_json(path_json_file)
    product_ids = df['id']

    for product_id in product_ids:
        path_Product = path_Data_Folder + str(category) + '/Products/p' + str(product_id) + '.json'
        # If product already exists, skip
        if os.path.exists(path_Product):
            continue
        # Get product
        response = requests.get(url.format(product_id), headers=headers, cookies=cookies, params=params)
        response.raise_for_status()

        # Save data to json file
        data = response.json()
        df_product = pd.DataFrame([data])
        df_product.to_json(path_Product, indent=2)
    return True

try:
    for index, row in product_ids.iterrows():
        category = row['URLKeys']
        print('Processing: ', category, end=' ')
        for page in range(1, 10):
            print(page, end=' ')
            if not extract_product(category, page) :
                break
        print()
        
    
except requests.exceptions.HTTPError as err:
    print('Error: ', err)
    print('Crawl product failed')
    raise