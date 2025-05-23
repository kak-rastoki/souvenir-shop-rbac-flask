import React, { useState, useEffect } from 'react';
import './CartPage.css';


function CartPage () {
  const [cart, setCart] = useState({ items: [], total_price: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect (() => {
    fetchCart();
  }, []);

  const fetchCart = () => {
    setLoading(true);
    fetch('http://localhost:5000/api/cart', {credentials:'include'})
      .then((response) => response.json())
      .then((data) => {
        setCart(data);
        setLoading(false);
      })
      .catch((err) => {
        setError('Ошибка при загрузке корзины');
        setLoading(false);
      });



  };

  const updateQuantity = (productId, quantity) => {
    fetch(`http://localhost:5000/api/cart/update/${productId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ quantity }),
      credentials:'include',
    })
      .then((response) => {
        if (!response.ok) throw new Error('Ошибка при обновлении');
        return fetchCart();
      })
      .catch((err) => {
        setError('Ошибка при обновлении количества');
      });
  };

  const removeFromCart = (productId) => {
    fetch(`http://localhost:5000/api/cart/remove/${productId}`, {
      method: 'DELETE',
      credentials:'include',
    })
      .then((response) => {
        if (!response.ok) throw new Error('Ошибка при удалении');
        return fetchCart();
      })
      .catch((err) => {
        setError('Ошибка при удалении товара');
      });
  };


  // Очистка корзины
  const clearCart = () => {
    fetch('http://localhost:5000/api/cart/clear', {
      method: 'DELETE',
      credentials:'include',
    })
      .then((response) => {
        if (!response.ok) throw new Error('Ошибка при очистке');
        return fetchCart();
      })
      .catch((err) => {
        setError('Ошибка при очистке корзины');
      });
  };

  const checkout = () => {
    fetch('http://localhost:5000/api/cart/checkout', {
      method: 'POST',
      credentials:'include',
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message === 'Заказ оформлен') {
          fetchCart();
          alert('Заказ успешно оформлен!');
        } else {
          throw new Error(data.error || 'Ошибка при оформлении');
        }
      })
      .catch((err) => {
        setError('Ошибка при оформлении заказа');
      });
  };

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="cart-page">
      <div className="cart-header">
        <h1>Ваша корзина</h1>
        {cart.items.length > 0 && (
          <div className="cart-info">
            <p>Товаров в корзине: {cart.items.length}</p>
            <button className="clear-cart-button" onClick={clearCart}>
              Очистить корзину
            </button>
          </div>
        )}
      </div>
      {cart.items.length === 0 ? (
        <p className="empty-cart">Ваша корзина пуста</p>
      ) : (
        <>
          <div className="cart-items">
            {cart.items.map((item) => (
              <div key={item.id} className="cart-item">
                <div className="item-image">
                  <img src={item.image} alt={item.name} />
                </div>
                <div className="item-details">
                  <h3>{item.name}</h3>
                  <p className="price">Цена: {item.price} ₽</p>
                </div>
                <div className="item-quantity">
                  <button
                    onClick={() => updateQuantity(item.product_id, item.quantity - 1)}
                  >
                    -
                  </button>
                  <span>{item.quantity}</span>
                  <button
                    onClick={() => updateQuantity(item.product_id, item.quantity + 1)}
                  >
                    +
                  </button>
                </div>
                <div className="item-total">
                  <p>Итого: {item.total} ₽</p>
                </div>
                <button
                  className="remove-item"
                  onClick={() => removeFromCart(item.product_id)}
                >
                  🗑️
                </button>
              </div>
            ))}
          </div>
          <div className="cart-summary">
            <h2>Общая стоимость: {cart.total_price} ₽</h2>
            <button className="checkout-button" onClick={checkout}>
              Оформить заказ
            </button>
          </div>
        </>
      )}
    </div>
  );
};




export default CartPage;
