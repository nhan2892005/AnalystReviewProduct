import axios from 'axios';
import SummaryReviews from '../models/summaryReviews.js';

export const getProductsbyId = async (req, res) => {
    const id = req?.params?.id;
    const field = ['id', 'name', 'url_path', 'short_url', 'short_description', 'price','list_price','original_price','badges_new','badges_v3','discount','discount_rate','rating_average','review_count','thumbnail_url','quantity_sold','description','current_seller','other_sellers','specifications','price_comparison','categories','benefits','return_policy']
    try {
        let params = {
            platform : 'web',
            spid : '271379452',
            version : 3
        }
        const response = await axios.get(`https://tiki.vn/api/v2/products/${id}`, { params });
        const data = response.data;
        const resp = field.reduce((obj, key) => {
            obj[key] = data[key];
            return obj;
        }, {});
        const res_model = await SummaryReviews.findOne({ name : id });
        if (res_model) {
            resp['summary'] = res_model['tóm tắt'];
        } else {
            resp['summary'] = 'Chưa tóm tắt review sản phẩm này';
        }
        res.status(200).json(resp);
    } catch (error){
        res.status(500).json({ message: error.message });
    }
}

export const getProductsbySearch = async (req, res) => {
    const searchQuery = req?.query?.query.replace(' ', '+');
    try {
        if (!searchQuery) {
            return res.status(400).json({ message: 'Invalid search query' });
        }
        let params = {
            limit: 40,
            include: 'advertisement',
            aggregations: 2,
            trackity_id: 'ecfa11b6-f624-60a3-3053-bcb700988447',
            q: searchQuery
        }
        const response = await axios.get('https://tiki.vn/api/v2/products', { params });
        const data = response.data;
        // for all products in data, map it with the following fields
        const field = ['id', 'name', 'url_path', 'seller_name', 'price', 'original_price', 'badges_new', 'badges_v3', 'discount', 'discount_rate', 'rating_average', 'review_count', 'thumbnail_url', 'thumbnail_width', 'thumbnail_height', 'quantity_sold', 'is_authentic', 'tiki_verified', 'tiki_hero'];
        const resp = data.data.map(product => {
            return field.reduce((obj, key) => {
                obj[key] = product[key];
                return obj;
            }, {});
        });
        resp.push({ length : resp.length });
        res.status(200).json(resp);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
}