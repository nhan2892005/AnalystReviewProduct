import axios from 'axios';

const API = axios.create({ baseURL: 'https://analystreviewproduct.onrender.com/' });

export const getProductsbySearch = (query) => API.get('products/search', { params: { query } });

export const getProductbyId = (id) => API.get(`products/${id}`);
