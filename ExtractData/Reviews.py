import pandas as pd
import re
import os
import sys
import datetime
from dbSchema import reviewSchema, customerSchema, commentSchema
from utils import add_record, store_to_df

path_category_ids = './CrawlData/CSVFile/URLKeys.csv'
path_Data_File = './CrawlData/Data_File/'
reviews = 'Reviews/'
comments = 'Comments'
path_record = './Records/'

categoryIds = pd.read_csv(path_category_ids)

try:
    for category in categoryIds['URLKeys'].iloc[:]:
        category_path = path_Data_File + str(category) +'/' + reviews
        path_record_category = path_record + str(category) + '/'
        print(category_path)
        for root, dirs, files in os.walk(category_path):
            for dir in dirs:
                if dir.startswith('review_'):
                    product_id = dir.split('_')[1]
                    review_dir = os.path.join(root, dir)
                    
                    json_files = [f for f in os.listdir(review_dir) if re.match(r'page_\d+\.json', f)]
                    for json_file in json_files:
                        file_path = os.path.join(review_dir, json_file)
                        if not os.path.exists(file_path):
                            continue
                        print(f'Reading: {file_path}')
                        
                        df = pd.read_json(file_path)
                        for i in range(len(df)):
                            row = df.iloc[i]
                            product_id = row.get('product_id')
                            
                            comments_data = row.get('comments', [])
                            review_comments = []
                            
                            if comments_data: 
                                for comment in comments_data:
                                    if not isinstance(comment, dict) or comment.get('id') is None:
                                        continue
                                    comment_id = comment['id']
                                    review_id = comment['review_id']
                                    commentator = comment['commentator']
                                    customer_id = comment['customer_id']
                                    fullname = comment['fullname']
                                    content = comment['content']
                                    score = comment['score']
                                    is_reported = comment['is_reported']

                                    review_comments.append(comment_id)
                                
                                    comment_data = [comment_id, review_id, commentator, customer_id, fullname, content, score, is_reported]
                                    comment_df = store_to_df(pd.DataFrame(columns=commentSchema.keys()), comment_data)
                                    comment_file = os.path.join(path_record_category, comments, f'p_{product_id}.json')
                                    
                                    add_record(comment_file, comment_df)
                            
                            id = row.get('id')
                            customer_id = row.get('customer_id')
                            product_id = row.get('product_id')
                            seller = row.get('seller') or {}
                            seller_id = seller.get('id')
                            title = row.get('title')
                            content = row.get('content')
                            status = row.get('status')
                            thank_count = row.get('thank_count')
                            score = row.get('score')
                            comment_count = row.get('comment_count')
                            rating = row.get('rating')
                            timeline = row.get('timeline') or {}
                            review_created_date = timeline.get('review_created_date')
                            delivery_date = timeline.get('delivery_date')
                            current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            relate_bought_and_review = timeline.get('explain')
                            vote_attributes = row.get('vote_attributes') or {}
                            agree = vote_attributes.get('agree')
                            disagree = vote_attributes.get('disagree')
                            
                            review_comments_str = ','.join(map(str, review_comments))
                            
                            review_data = [id, customer_id, product_id, seller_id, title, content, status, thank_count, score, comment_count, rating, review_created_date, delivery_date, current_date, relate_bought_and_review, agree, disagree, review_comments_str]
                            review_df = store_to_df(pd.DataFrame(columns=reviewSchema.keys()), review_data)
                            
                            add_record(path_record_category + reviews + 'p_' + str(product_id) + '.json', review_df)
                            
                            # New code for processing customer data
                            customer = row.get('created_by') or {}
                            customer_id = customer.get('id')
                            customer_name = customer.get('name')
                            customer_full_name = customer.get('full_name')
                            customer_region = customer.get('region')
                            customer_created_time = customer.get('created_time')  # Sử dụng .get() để tránh KeyError
                            customer_purchased = customer.get('purchased')
                            customer_contribute = customer.get('contribute_info', {}) or {}
                            customer_summary = customer_contribute.get('summary', {}) or {}
                            customer_joined_time = customer_summary.get('joined_time')
                            customer_total_review = customer_summary.get('total_review')
                            customer_total_thank = customer_summary.get('total_thank')

                            customer_data = [
                                customer_id, 
                                customer_name, 
                                customer_full_name, 
                                customer_region, 
                                customer_created_time, 
                                customer_purchased, 
                                customer_joined_time, 
                                customer_total_review, 
                                customer_total_thank
                            ]

                            # Lọc bỏ các giá trị None từ customer_data
                            customer_data = [value if value is not None else '' for value in customer_data]
                            customer_df = store_to_df(pd.DataFrame(columns=customerSchema.keys()), customer_data)
                            
                            if customer_created_time:
                                created_date = datetime.datetime.strptime(customer_created_time, '%Y-%m-%d %H:%M:%S')
                                file_suffix = f"{created_date.month:02d}_{created_date.year}"
                            else:
                                file_suffix = "unknown_date"

                            customer_file = os.path.join(path_record_category + 'Users/', f'users_{file_suffix}.json')

                            add_record(customer_file, customer_df)
        
except Exception as e:
    print(f"Lỗi không xác định: {e}")
    print(f"Chi tiết lỗi: {repr(e)}")        
