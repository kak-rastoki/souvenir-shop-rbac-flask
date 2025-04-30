import React from 'react';
import './ProductCard.css';
import BeerImage from './Beer1.png';


function ProductCard({product}) {


  return (
    <div className="product-card">

      <img src={`data:image/jpeg;base64,${product.image}`} alt={product.name} />
      <h3>{product.name}</h3>
      <div className = 'card-group'>
        <div className='group-category-more'>
          <p className="category">{product.category}</p>
          <a  href="#" className="more">Подробнее</a>
        </div>
        <div className='group-bt-price'>
          <p className="price">{product.price} ₽</p>
          <button>В корзину</button>
        </div>
      </div>
    </div>
  )
};


export default ProductCard
