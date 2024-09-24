document.addEventListener('DOMContentLoaded', function() {

  const cartButton = document.querySelector('#mnhd-cart a');
  const cartBlock = document.getElementById('cart-block');
  const cartItemsList = document.getElementById('cart-items');
  const clearCartButton = document.querySelector('.cart-but-del'); // Новое

  // Проверим, что элементы найдены, и добавим обработчик клика
  if (cartButton && cartBlock) {
      cartButton.addEventListener('click', function(event) {
          event.preventDefault();
          cartBlock.classList.toggle('visible');
      });
  } else {
      console.error("Cart button or cart block not found.");
  }


  if (clearCartButton && cartItemsList) {
    clearCartButton.addEventListener('click', function(event) {
        event.preventDefault();
        clearCart();
    });
} else {
    console.error("Clear cart button or cart items list not found.");
}


function clearCart() {
  while (cartItemsList.firstChild) {
      cartItemsList.removeChild(cartItemsList.firstChild);
  }

  // Показать сообщение "Ваша корзина пуста" после очистки
  const cartNoneMessage = document.getElementById('cart-none');
  if (cartNoneMessage) {
      cartNoneMessage.style.display = 'block';
  }
}
  // Найдем все кнопки "Add to Cart"
  //!новое
  const addToCartButtons = document.querySelectorAll('.add-to-cart');

  // Цикл по всем кнопкам "Add to Cart"
  addToCartButtons.forEach(button => {
      // Добавляем обработчик события "click" для каждой кнопки
      button.addEventListener('click', function(event) {
          // Предотвращаем стандартное поведение кнопки (например, переход по ссылке)
          event.preventDefault();

          // Получаем данные товара из атрибутов кнопки
          const productId = button.getAttribute('data-id');
          const productName = button.getAttribute('data-name');
          const productPrice = button.getAttribute('data-price');

          //!отладка
          // Логируем данные, которые будут отправлены на сервер
          console.log('Отправлен запрос серверу с данными:', {
              id: productId,
              name: productName,
              price: productPrice
          });

          // Отправляем AJAX-запрос на сервер
          fetch('/add_to_cart', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCookie('csrf_token') // Добавляем CSRF-токен
              },
              // Преобразуем данные товара в JSON
              body: JSON.stringify({
                  id: productId,
                  name: productName,
                  price: productPrice
              })
          })
          //!новое
          .then(response => {
              // Логируем ответ от сервера
              console.log('Ответ сервера:', response);
              // Проверяем, успешен ли ответ
              if (!response.ok) {
                  throw new Error('Network response was not ok');
              }
              // Преобразуем ответ в JSON
              return response.json();
          })
          .then(data => {
              // Обрабатываем данные ответа
              if (data.success) {
                  console.log('Товар добавлен в корзину: ' + productName + " "+ productPrice + " P");
                  addItemToCart(productId, productName, productPrice);
                  // Здесь можно обновить отображение корзины, если необходимо
              } else {
                  console.error('Ошибка добавления товара:', data.error);
              }
          })
          // Обрабатываем ошибки запроса
          .catch(error => console.error('Ошибка:', error));
      });
  });

    // Функция для добавления товара в корзину на клиенте
    function addItemToCart(id, name, price) {
      const cartItem = document.createElement('li');
      cartItem.textContent = `${name} - ${price} ₽`;
      cartItem.setAttribute('data-id', id);
      cartItemsList.appendChild(cartItem);

      // Убираем сообщение "Ваша корзина пуста", если оно есть
      const cartNoneMessage = document.getElementById('cart-none');
      if (cartNoneMessage) {
          cartNoneMessage.style.display = 'none';
      }
  }




});



// Функция для получения CSRF-токена из куки
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
