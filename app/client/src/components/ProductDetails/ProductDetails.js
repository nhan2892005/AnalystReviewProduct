import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { getProductById } from '../../actions';
import './ProductDetails.css'; 
import { useParams } from 'react-router-dom';

const ProductDetails = ({ match }) => {
    const { id } = useParams(); 
    const dispatch = useDispatch();
    const product = useSelector(state => state.products.product);

    useEffect(() => {
        dispatch(getProductById(id));
    }, [dispatch, id]);

    if (!product) {
        return <div>Loading...</div>;
    }

    const processText = (text) => {
        const sections = text.split(/(?=\*\*|\*\s)/);
        return sections
            .map(section => {
                if (section.startsWith('**')) {
                    return `<h4>${section.slice(2).trim()}</h4>`; 
                } else if (section.startsWith('*')) {
                    return `<p>${section.slice(1).trim()}</p>`; 
                }
                return ''; 
            })
            .join('');
    };

    return (
        <div className="product-details">
            <h1 className="product-title">{product.name}</h1>
            <img className="product-image" src={product.thumbnail_url} alt={product.name} />
            <div className="product-price">
                <span className="current-price">{product.price.toLocaleString()} ₫</span>
                <span className="list-price">{product.list_price.toLocaleString()} ₫</span>
                <span className="discount-rate">{product.discount_rate}%</span>
            </div>
            <div className="badges">
                {product.badges_new.map(badge => (
                    <div key={badge.code} className="badge">
                        {badge.icon && <img className="badge-icon" src={badge.icon} alt={badge.text} />}
                        {badge.text && <span>{badge.text}</span>}
                    </div>
                ))}
            </div>
            <h2 className="details-title">Thông tin chi tiết</h2>
            <div className="details-content" dangerouslySetInnerHTML={{ __html: product.description }} />
            <h3 className="supplier-title">Nhà cung cấp</h3>
            <p className="supplier-name">{product.current_seller.name}</p>
            <h3 className="supplier-title">Tóm tắt đánh giá sản phẩm</h3>
            <p className="supplier-rating" dangerouslySetInnerHTML={{ __html: processText(product.summary) }} />
            <a className="supplier-link" href={product.current_seller.link} target="_blank" rel="noopener noreferrer">Xem thêm</a>
        </div>
    );
};

export default ProductDetails;
