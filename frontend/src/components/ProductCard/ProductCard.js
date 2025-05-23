import React, {useState,useEffect} from 'react';
import './ProductCard.css';
import { Link } from 'react-router-dom';





function ProductCard({product,animationDelay}) {
  const [addingToCart, setAddingToCart] = useState(false);

  const addToCart = () => {
    setAddingToCart(true);
    fetch('http://localhost:5000/api/cart/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: product.id, quantity: 1 }),
        credentials:'include',
    })
        .then(response => {
            if (!response.ok) {
                return response.json()
                    .then(err => { throw new Error(err.error || 'Ошибка добавления в корзину') });
            }
            return response.json();
        })
        .then(data => {
            console.log('Товар добавлен:', data);
            alert('Товар успешно добавлен в корзину!');
            setAddingToCart(false);
        })
        .catch(err => {
            console.error('Ошибка:', err.message);
            alert(`Ошибка: ${err.message}`);
            setAddingToCart(false);
        });
    };

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
          <button onClick={addToCart} disabled={addingToCart}>{addingToCart ? 'Добавляем...' : 'В корзину'}</button>
        </div>
      </div>
    </div>

  )
};


export default ProductCard
