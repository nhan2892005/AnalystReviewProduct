import pandas as pd
productSchema = pd.DataFrame([{
    'id': 'None',
    'name': 'None',
    'description': 'None',
    'price': 'None',
    'brandId': 'None',
    'sellerId': 'None',
    'categoryId': 'None',
    'discount': 'None',
    'rating_average': 'None',
    'review_count': 'None',
    'price_comparison': 'None',
    'stars': 'None',
}])

brandSchema = pd.DataFrame([{
    'id': 'None',
    'name': 'None',
    'slug': 'None',
}])

brandSchema = pd.DataFrame([{
    'id': 'None',
    'name': 'None',
    'is_best_store': 'None',
}])

categorySchema = pd.DataFrame([{
    'id': 'None',
    'name': 'None',
}])

reviewSchema = pd.DataFrame([{
    'id' : 'None',
    'customer_id' : 'None',
    'product_id' : 'None',
    'seller_id' : 'None',
    'title' : 'None',
    'content' : 'None',
    'status' : 'None',
    'thank_count' : 'None',
    'score' : 'None',
    'comment_count' : 'None',
    'rating' : 'None',
    'review_created_date' : 'None',
    'delivery_date' : 'None',
    'current_date' : 'None',
    'relate_bought_and_review' : 'None',
    'agree' : 'None',
    'disagree' : 'None',
    'review_comments' : 'None',
}])

customerSchema = pd.DataFrame([{
    'customer_id': 'None',
    'customer_name': 'None',
    'customer_full_name': 'None',
    'customer_region': 'None',
    'customer_created_time': 'None',
    'customer_purchased': 'None',
    'customer_joined_time': 'None',
    'customer_total_review': 'None',
    'customer_total_thank': 'None',
}])

commentSchema = pd.DataFrame([{
    'comment_id': 'None',
    'review_id': 'None',
    'commentator': 'None',
    'customer_id': 'None',
    'fullname': 'None',
    'content': 'None',
    'score': 'None',
    'is_reported': 'None',
}])
