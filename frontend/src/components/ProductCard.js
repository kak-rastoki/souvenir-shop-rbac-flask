import React from 'react';
import './ProductCard.css';
import BeerImage from './Beer1.png';


function ProductCard({product}) {


  return (
    <div className="product-card">

      <img src={BeerImage} alt="Карточка товара" width="200px" />
      <h3>Статуетка медведя</h3>
      <div className = 'card-group'>
        <p className="category">сувениры</p>
        <p className="price">2600 ₽</p>
      </div>
      <button>В корзину</button>

    </div>
  )
}


export default ProductCard
