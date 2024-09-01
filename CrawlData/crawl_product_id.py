import requests
import csv
from cookies_and_headers import cookies, headers
import os
from module_process_csv import read_csv_file

os.makedirs('./CrawlData/CSVFile', exist_ok=True)

url='https://tiki.vn/api/personalish/v1/blocks/listings'

params = {
    'limit' : '40',
    'include' : 'advertisement',
    'aggregations' : '2',
    'version' : 'home-persionalized',
    'trackity_id' : 'ecfa11b6-f624-60a3-3053-bcb700988447',
    'category' : '8322',
    'page' : '1',
    'urlKey' : 'nha-sach-tiki',
}

# Read URLKeys from CSV File
url_keys = read_csv_file('URLKeys.csv')

try:
    for _, row in url_keys.iterrows():
        params['urlKey'] = row['URLKeys']
        params['category'] = row['Category']
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        response.raise_for_status()
        total_page = response.json()['paging']['last_page']
        for i in range(1, total_page + 1):
            params['page'] = str(i)
            response = requests.get(url, headers=headers, cookies=cookies, params=params)
            response.raise_for_status()
            data = response.json()['data']
            with open('./CrawlData/CSVFile/ProductID.csv', mode='a', newline='', encoding='utf-8') as file:
                
                writer = csv.writer(file)
                
                writer.writerow(['Product_ID'])

                for item in data:
                    writer.writerow([item['id']])

except requests.exceptions.HTTPError as err:
    print('Error: ', err)
    print('Crawl listing failed')
    raise
