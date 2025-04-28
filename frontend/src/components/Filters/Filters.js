import React from 'react'
import './Filters.css'

function Filters () {



return (
  <div className="filters">
    <div className='block'>
      <h3>Настройки поиска</h3>

      <input name="search" id='search' type="text"/>
      <button>Сбросить фильтрацию</button>
      <div className='group'>
        <input name="checkbox1" type="checkbox" className='checkbox'/>
        <label for="checkbox1">Есть в наличии</label>
      </div>
    </div>

    <div className='block'>
      <label className='label-price'>Цена</label>
      <div className='group flex-group'>
        <input id="price-from" placeholder= "от" type="text"/>
        <input  id="price-to" placeholder= "до" type="text"/>
      </div>
      <div className='group'>
        <input type="radio" name="price-type" />
        <label for="price-type">Сначала дороже</label>
      </div>
      <div className='group'>
        <input type="radio" name="price-type" />
        <label for="price-type">Сначала дешевле</label>
      </div>
    </div>

    <div className='block'>
      <label>Популярность</label>
      <div className='group'>
        <input type="radio" name="popularity-type" />
        <label for="popularity-type">Сначала популярнее</label>
      </div>
      <div className='group'>
        <input type="radio" name="popularity-type" />
        <label for="popularity-type">Сначала непопулярные</label>
      </div>
    </div>

    <button>Применить</button>



  </div>

);
};


export  default Filters
