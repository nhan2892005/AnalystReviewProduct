import axios from 'axios';

const API = axios.create({ baseURL: 'http://localhost:5000' });

export const getProductsbySearch = (query) => API.get('products/search', { params: { query } });

export const getProductbyId = (id) => API.get(`products/${id}`);
