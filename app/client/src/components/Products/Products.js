import React from 'react';
import { useSelector } from 'react-redux';
import ProductCard from './Product/Product'; 

const Products = () => {
  const products = useSelector((state) => state.products.search); 
  const loading = useSelector((state) => state.loading); 
  const error = useSelector((state) => state.error); 

  console.log(products);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <div style={styles.container}>
      {products && products.length > 0 ? (
        products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))
      ) : (
        <p>Không có sản phẩm nào để hiển thị</p>
      )}
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    padding: '16px',
  },
};

export default Products;
