import React, { useState } from 'react'
import './Filters.css'



function Filters ({priceFilterChange}) {
const [minPrice, setMinPrice] = useState('');
const [maxPrice, setMaxPrice] = useState('');

const handlePriceFilterChange = (newMinPrice,newMaxPrice) => {
  priceFilterChange(newMinPrice,newMaxPrice);
}


return (
  <div className="filters">
    <div className='block'>
      <h3>Настройки поиска</h3>

      <input name="search" id='search' type="text"/>
      <button>Сбросить фильтрацию</button>
      <div className='group'>
        <input name="checkbox1" type="checkbox" className='checkbox'/>
        <label htmlFor="checkbox1">Есть в наличии</label>
      </div>
    </div>

    <div className='block'>
      <label className='label-price'>Ценовой диапозон в руб.</label>
      <div className='group flex-group'>
        <input id="price-from" placeholder= "от" type="number" value={minPrice}
        onChange={(e)=>{
          const newMinPrice = e.target.value;
          setMinPrice (e.target.value);
          handlePriceFilterChange(newMinPrice, maxPrice);
         }}/>
        <input  id="price-to" placeholder= "до" type="number" value={maxPrice}
        onChange={(e)=>{
          const newMaxPrice = e.target.value;
          setMaxPrice (e.target.value);
          handlePriceFilterChange(minPrice, newMaxPrice);
         }}/>
      </div>
      <div className='group'>
        <input type="radio" name="price-type" />
        <label htmlFor="price-type">Сначала дороже</label>
      </div>
      <div className='group'>
        <input type="radio" name="price-type" />
        <label htmlFor="price-type">Сначала дешевле</label>
      </div>
    </div>

    <div className='block'>
      <label>Популярность</label>
      <div className='group'>
        <input type="radio" name="popularity-type" />
        <label htmlFor="popularity-type">Сначала популярнее</label>
      </div>
      <div className='group'>
        <input type="radio" name="popularity-type" />
        <label htmlFor="popularity-type">Сначала непопулярные</label>
      </div>
    </div>

    <button>Применить</button>



  </div>

);
};


export  default Filters
