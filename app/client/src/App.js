import React from 'react';
import { Container } from '@mui/system';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import Navbar from './components/Navbar/NavBar';
import Home from './components/Home/Home';
import Products from './components/Products/Products';
import ProductDetails from './components/ProductDetails/ProductDetails';

const App = () => {
  return (
    <BrowserRouter>
      <Container maxWidth="lg">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} /> {}
          <Route path="/search" element={<Products />} /> {}
          <Route path="/product/:id" element={<ProductDetails />} /> {}
        </Routes>
      </Container>
    </BrowserRouter>
  );
};

export default App;
