import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { getProductById } from '../../../actions';

const ProductCard = ({ product }) => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleViewDetails = () => {
    dispatch(getProductById(product.id));
    navigate(`/product/${product.id}`);
  };



  return (
    <div style={styles.card}>
      <img src={product.thumbnail_url} alt={product.name} style={styles.image} />
      <div style={styles.content}>
        <h3 style={styles.name}>{product.name}</h3>
        <p style={styles.seller}>Người bán: {product.seller_name}</p>
        
        {/* Kiểm tra giá trước khi sử dụng toLocaleString */}
        <p style={styles.price}>Giá: {product.price ? product.price.toLocaleString() : 'N/A'}₫</p>
        {product.original_price !== product.price && (
          <p style={styles.originalPrice}>
            Giá gốc: {product.original_price ? product.original_price.toLocaleString() : 'N/A'}₫
          </p>
        )}
        
        <p style={styles.rating}>
          Đánh giá: {product.rating_average} ⭐ ({product.review_count} nhận xét)
        </p>
        
        {product.quantity_sold && (
          <p style={styles.sold}>Đã bán: {product.quantity_sold.text}</p>
        )}

        {/* */}
        {product.badges_new && product.badges_new.length > 0 && (
          <div style={styles.badges}>
            {product.badges_new.map((badge, index) => (
              <div key={index} style={styles.badge}>
                {badge.type === 'icon_badge' && (
                  <img src={badge.icon} alt="badge" style={styles.badgeIcon} />
                )}
                {badge.type === 'delivery_info_badge' && (
                  <p>{badge.text}</p>
                )}
                {badge.type === 'icon_text_promotion' && badge.promotions.map((promo, i) => (
                  <p key={i} style={styles.promo}>
                    <img src={promo.icon} alt="promotion" style={styles.promoIcon} />
                    {promo.text}
                  </p>
                ))}
              </div>
            ))}
          </div>
        )}
        <button onClick={handleViewDetails} style={styles.button}>
          Xem chi tiết
        </button>
      </div>
    </div>
  );
};


const styles = {
  card: {
    border: '1px solid #ddd',
    borderRadius: '8px',
    padding: '16px',
    maxWidth: '320px',
    margin: '16px',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
  },
  image: {
    width: '100%',
    height: 'auto',
    borderRadius: '8px',
  },
  content: {
    marginTop: '12px',
  },
  name: {
    fontSize: '18px',
    fontWeight: 'bold',
  },
  seller: {
    color: '#555',
  },
  price: {
    color: '#E53935',
    fontSize: '18px',
    fontWeight: 'bold',
  },
  originalPrice: {
    textDecoration: 'line-through',
    color: '#888',
  },
  rating: {
    color: '#FFC107',
  },
  sold: {
    color: '#4CAF50',
  },
  badges: {
    marginTop: '8px',
  },
  badge: {
    marginRight: '8px',
  },
  badgeIcon: {
    width: '89px',
    height: '20px',
  },
  promo: {
    color: '#F44336',
    fontSize: '14px',
    display: 'flex',
    alignItems: 'center',
  },
  promoIcon: {
    width: '16px',
    height: '16px',
    marginRight: '4px',
  },
  button: {
    display: 'inline-block',
    marginTop: '12px',
    padding: '8px 16px',
    backgroundColor: '#FF5722',
    color: 'white',
    textDecoration: 'none',
    borderRadius: '4px',
    textAlign: 'center',
  },
};

export default ProductCard;
