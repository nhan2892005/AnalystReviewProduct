import requests
import csv
from cookies_and_headers import cookies, headers
import os
from module_process_csv import read_csv_file
from module_delete_htmlTag import remove_html_tags

os.makedirs('./CrawlData/CSVFile', exist_ok=True)

url='https://tiki.vn/api/v2/products/{}'

params = {
    'platform' : 'web',
    'spid' : '10853528',
    'version' : '3',
}

# Read Product_IDs from CSV File
product_ids = read_csv_file('ProductID.csv')

try:
    with open('./CrawlData/CSVFile/Products.csv', mode='w', newline='', encoding='utf-8') as file:       
        writer = csv.writer(file)
        writer.writerow(['Product_ID', 'Product_Name', 'Price', 'Price_comparrison', 'Category','Benefits'])
        for idx, row in product_ids.iterrows():
            if (idx + 1) % 1000 == 0:
                print('Crawled: {}/{} ({}%)'.format(idx + 1, len(product_ids), round((idx + 1) / len(product_ids) * 100, 2)))
            response = requests.get(url.format(row['Product_ID']), headers=headers, cookies=cookies, params=params)
            response.raise_for_status()
            data = response.json()

            # Check if the product has no review, no price comparison, no categories, no benefits
            if data['review_count'] == 0:
                continue
            if 'price_comparison' not in data:
                data['price_comparison'] = {'sub_title': 'None'}
            if 'categories' not in data:
                data['categories'] = {'name': 'None'}
            if 'benefits' not in data:
                data['benefits'] = [{'text': 'None'}]
            
            writer.writerow([data['id'], data['name'], data['price'], data['price_comparison']['sub_title'], data['categories']['name'], [benefit['text'] for benefit in data['benefits']]])
except requests.exceptions.HTTPError as err:
    print('Error: ', err)
    print('Crawl product failed')
    raise