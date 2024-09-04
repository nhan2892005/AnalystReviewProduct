import pandas as pd
import os
from utils import add_record, get_relate_record

path_category_ids = './CrawlData/CSVFile/URLKeys.csv'
path_Data_File = './CrawlData/Data_File/'
products = 'Products/'

categoryIds = pd.read_csv(path_category_ids)

def get_product(folder_path, path_Record):
    '''
    Loop through all files in the folder and get their names and content
    '''
    for _, _, files in os.walk(folder_path):
        length = len(files)
        for index, file in enumerate(files, start=1):
            print(f'{index}/{length} = {round(index * 100 / length, 2)}%')
            
            df = pd.read_json(folder_path + file)

            # Get related records
            brandRec = get_relate_record(df, 'brand', ['id', 'name', 'slug'])
            add_record(path_Record + 'brands.json', brandRec)

            sellerRec = get_relate_record(df, 'current_seller', ['id', 'name', 'is_best_store'])
            add_record(path_Record + 'sellers.json', sellerRec)

            categoryRec = get_relate_record(df, 'categories', ['id', 'name'])
            add_record(path_Record + 'categories.json', categoryRec)
            
            try:
                id = df['id'].iloc[0]
            except (KeyError, IndexError, TypeError):
                id = 'None'
            try:
                name = df['name'].iloc[0]
            except (KeyError, IndexError, TypeError):
                name = 'None'
            try:
                description = df['description'].iloc[0]
            except (KeyError, IndexError, TypeError):
                description = 'None'
            try:
                price = df['price'].iloc[0]
            except (KeyError, IndexError, TypeError):
                price = 'None'
            try:
                brandId = df['brand'].iloc[0]['id']
            except (KeyError, IndexError, TypeError):
                brandId = 'None'
            try:
                sellerId = df['current_seller'].iloc[0]['id']
            except (KeyError, IndexError, TypeError):
                sellerId = 'None'
            try:
                categoryId = df['categories'].iloc[0]['id']
            except (KeyError, IndexError, TypeError):
                categoryId = 'None'
            try:
                discount = df['discount'].iloc[0]
            except (KeyError, IndexError, TypeError):
                discount = 'None'
            try:
                rating_average = df['rating_average'].iloc[0]
            except (KeyError, IndexError, TypeError):
                rating_average = 'None'
            try:
                review_count = df['review_count'].iloc[0]
            except (KeyError, IndexError, TypeError):
                review_count = 'None'
            try:
                price_comparison = df['price_comparison'].iloc[0]['subtitle']
            except (KeyError, IndexError, TypeError):
                price_comparison = 'None'
            try:
                reviewFile = folder_path.replace('Products', 'Reviews') + 'review_' + str(id) + '/' + 'overview.json' 
                if os.path.exists(reviewFile):
                    review_df = pd.read_json(reviewFile)
                    stars = review_df['stars'].iloc[0]
                else:
                    stars = 'None'
            except (KeyError, IndexError, TypeError):
                stars = 'None'
            
            print('Get Fields: Done')

            productRec = pd.DataFrame([{
                'id': id,
                'name': name,
                'description': description,
                'price': price,
                'brandId': brandId,
                'sellerId': sellerId,
                'categoryId': categoryId,
                'discount': discount,
                'rating_average': rating_average,
                'review_count': review_count,
                'price_comparison': price_comparison,
                'stars': stars
            }])

            add_record(path_Record + 'products.json', productRec, info_num_record=True)
            print('------Add Record: Done------')

for _, row in categoryIds.iloc[2:].iterrows():
    category = row['URLKeys']
    path = path_Data_File + str(category) + '/' + products
    path_Record = './Records/' + str(category) + '/'
    if os.path.exists(path):
        if not os.path.exists(path_Record):
            os.makedirs(path_Record, exist_ok=True)
        get_product(path_Data_File + str(category) + '/' + products, path_Record)
    print('Done: ' + category)
