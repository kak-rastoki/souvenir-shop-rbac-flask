
import logo from './logo.svg';
import Catalog from './components/Catalog/Catalog'
import ProductPage from './components/ProductPage/ProductPage';
import './App.css';
import { Routes, Route } from 'react-router-dom';


function App() {
  return (
    <Routes>
      <Route path="/" element={<Catalog />} />
      <Route path="/product/:id" element={<ProductPage />} />
    </Routes>
  );

}

export default App;
