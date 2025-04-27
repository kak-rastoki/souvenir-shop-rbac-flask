import React from 'react'
import './Filters.css'

function Filters () {



return (
  <div className="filters">
    <h3>Настройки поиска</h3>
    <input type="text"/>
    <div className='group'>
      <input type="checkbox" className='checkbox'/>
      <label>Есть в наличии</label>
    </div>
    <label className='label-price'>Цена</label>
    <div className='group flex-group'>
      <input id="price-from" placeholder= "от" type="text"/>
      <input  id="price-to" placeholder= "до" type="text"/>
    </div>

  </div>

);
};


export  default Filters
