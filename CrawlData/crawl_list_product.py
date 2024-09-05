import requests
from cookies_and_headers import cookies, headers
import os
from utils import read_csv_file
import pandas as pd

# ! Objective: Crawl all product in page category
# ! Store Data: ./CrawlData/Data_File/{category}/page_{page_of_list_product}.json

# Directory to store crawl data
path_Folder_Data = './CrawlData/Data_File/'
os.makedirs(path_Folder_Data, exist_ok=True)

# URL of API
url='https://tiki.vn/api/personalish/v1/blocks/listings'

params = {
    'limit' : '300',
    'include' : 'advertisement',
    'aggregations' : '2',
    'version' : 'home-persionalized',
    'trackity_id' : 'ecfa11b6-f624-60a3-3053-bcb700988447',
    'category' : '8322',
    'page' : '1',
    'urlKey' : 'nha-sach-tiki',
}


# Read URLKeys from CSV File
url_keys = pd.read_csv('./CrawlData/CSVFile/URLKeys.csv')

try:
    for _, row in url_keys.iterrows():

        # Create folder base on category
        os.makedirs(path_Folder_Data + str(row['URLKeys']), exist_ok=True)

        # Update params with new URLKeys
        params['urlKey'] = row['URLKeys']
        params['category'] = row['Category']

        # Get total page
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        response.raise_for_status()
        total_page = response.json()['paging']['last_page']

        # Loop for crawl data and save to json file
        for i in range(1, int(total_page) + 1):

            # Update params and access to URL
            params['page'] = str(i)
            response = requests.get(url, headers=headers, cookies=cookies, params=params)
            response.raise_for_status()

            # Save data to json file
            data = response.json()['data']
            df = pd.DataFrame(data)
            df.to_json(path_Folder_Data + str(row['URLKeys']) + '/page_' + str(i) + '.json', indent=2)
except requests.exceptions.HTTPError as err:
    print('Error: ', err)
    print('Crawl listing failed')
    raise
