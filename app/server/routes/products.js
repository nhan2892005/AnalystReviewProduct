import express from 'express';
import { getProductsbySearch, getProductsbyId } from '../controllers/products.js';
const router = express.Router();

router.get('/search', getProductsbySearch);
router.get('/:id', getProductsbyId);

export default router;
