import React from 'react';
import './ProductCard.css';
import BeerImage from './Beer1.png';


function ProductCard({product}) {


  return (
    <div className="product-card">

      <img src={BeerImage} alt="Карточка товара" />
      <h3>Статуетка медведя</h3>
      <div className = 'card-group'>
        <div className='group-category-more'>
          <p className="category">Сувениры</p>
          <a  href="#" className="more">Подробнее</a>
        </div>
        <div className='group-bt-price'>
          <p className="price">2600 ₽</p>
          <button>В корзину</button>
        </div>
      </div>


    </div>
  )
}


export default ProductCard
