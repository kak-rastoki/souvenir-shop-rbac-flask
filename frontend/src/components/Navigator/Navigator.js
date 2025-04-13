import React from 'react';
import './Navigator.css'

function Navigator(){

  return(
    <div class='navigator-wrapper'>
      <div class="navigator">
        <div class="woody-products">
          <h3 id="woody-h3">Изделия из дерева</h3>
          <ul className='category-ul'>
            <li><button>Сувениры</button></li>
            <li><button>Бытовая продукция</button></li>
            <li><button>Корпусная мебель</button></li>
            <li><button>Картины</button></li>
          </ul>
        </div>
        <div class="metal-products">
          <h3 id="metal-h3">Изделия из металла</h3>
          <ul className='category-ul'>
            <li><button>Мангалы</button></li>
            <li><button>Печи</button></li>
          </ul>

        </div>
        <button id="new-products-bt">НОВИНКИ</button>
      </div>

    </div>

  );
};





export default Navigator
