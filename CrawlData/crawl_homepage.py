import requests
import csv
import os
from cookies_and_headers import cookies, headers
from urllib.parse import urlparse

# Get Product Categories URL

url = 'https://api.tiki.vn/raiden/v2/menu-config'

os.makedirs('./CrawlData/CSVFile', exist_ok=True)

try:
    # Send a GET request to the homepage
    response = requests.get(url, headers=headers, cookies=cookies)
    response.raise_for_status()

    # Get the items from the response
    items = response.json()['menu_block']['items']
    
    # Open a CSV file in write mode
    with open('./CrawlData/CSVFile/URLKeys.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(['URLKeys', 'Category'])
        
        # With each item, extract the URLKeys and CategoryID
        for item in items:
            # Get the URLKeys and CategoryID
            # Ex: https://tiki.vn/dien-thoai-may-tinh-bang/c1789 => dien-thoai-may-tinh-bang, 1789
            parsed_url = urlparse(item['link'])
            path_segments = parsed_url.path.split('/')
            writer.writerow([path_segments[1], int(path_segments[2][1:])])
    
    print('Links have been written to links.csv')

except requests.exceptions.HTTPError as err:
    print('Error: ', err)
    print('Crawl homepage failed')
    raise
