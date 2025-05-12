import React from 'react';
import './ProductCard.css';
import { Link } from 'react-router-dom';



function ProductCard({product,animationDelay}) {


  return (

    <div className="product-card" style={{ animationDelay: `${animationDelay}s` }}>
      <div className='img-container'>
        <Link to={`/product/${product.id}`}>
        <img src={`data:image/jpeg;base64,${product.image}`} alt={product.name} />
        </Link>
      </div>
      <div className='product-title'>
        <h3>{product.name}</h3>
      </div>
      <div className = 'card-group'>
        <div className='group-category-more'>
          <p className="category">{product.category}</p>
          <Link to={`/product/${product.id}`} className="more">Подробнее</Link>
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
