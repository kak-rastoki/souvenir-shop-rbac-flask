import React from 'react';
import './AddToCartModal.css'


function AddToCartModal ({isOpen, onClose}) {
  if (!isOpen) return null;

  return (
    <div className='modal-addtocart'>
      <div className='content modal-enter'>
        <p>✅ Товар добавлен в корзину</p>
      </div>
    </div>
  )


}

export default AddToCartModal;
