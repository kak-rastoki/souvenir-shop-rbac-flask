import React from "react";
import "./CheckoutModal.css"

function CheckoutModal ({showCheckoutModal, closeCheckoutModal,orderId }) {

  if (!showCheckoutModal) return null;

  return (
    <div className="modal-overlay" onClick={closeCheckoutModal}>
      <div className="modal-checkout" onClick={(e) => e.stopPropagation()}>
        <div className="content modal-enter">
          <h2>Ваш заказ оформлен</h2>
          <div className="number-group">
            <p>Номер заказа:</p>
            <div className="checkoutIdfield">
              <p>{orderId || 'Загрузка...'}</p>
            </div>
          </div>
          <button className="close-button" onClick={closeCheckoutModal}>
            ✖
          </button>
        </div>
      </div>
    </div>
  );
}


export default CheckoutModal;
