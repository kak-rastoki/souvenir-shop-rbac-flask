import React, { useState,useEffect } from 'react';
import './Navigator.css'




function Navigator(){
  const [selectedCategory,setSelectedCategory] = useState('Новинки');
  const [material,setMaterial] = useState ('Изделия из дерева');

  // let wood = ["Сувениры","Бытовая продукция","Корпусная мебель","Картины"]
  let metal = ["Мангалы","Печи"];

  useEffect(() => {
    if (metal.includes(selectedCategory)) {
      setMaterial("Изделия из металла");

    } else {
      setMaterial("Изделия из дерева");

    }
  }, [selectedCategory]);


  return(
    <div className='navigator-wrapper'>
      <div className="navigator">
        <div className="woody-products">
          <h3 id="woody-h3">Изделия из дерева</h3>
          <ul className='category-ul'>
            <li><button onClick={()=> setSelectedCategory("Сувениры")}>Сувениры</button></li>
            <li><button  onClick={()=> setSelectedCategory("Бытовая продукция")}>Бытовая продукция</button></li>
            <li><button  onClick={()=> setSelectedCategory("Корпусная мебель")}>Корпусная мебель</button></li>
            <li><button  onClick={()=> setSelectedCategory("Картины")}>Картины</button></li>
          </ul>
        </div>
        <div className="metal-products">
          <h3 id="metal-h3">Изделия из металла</h3>
          <ul className='category-ul'>
            <li><button onClick={()=> setSelectedCategory("Мангалы")}>Мангалы</button></li>
            <li><button onClick={()=> setSelectedCategory("Печи")}>Печи</button></li>
          </ul>

        </div>
        <button id="new-products-bt">НОВИНКИ</button>
      </div>

      <div className='bread-crumbs'>
        <a href="#">Магазин студенческий</a>
        <p>-></p>
        <a href="#">Каталог</a>
        <p>-></p>
        <a href="#" className="breadcrumb-item" key={material}>{material}</a>
        <p>-></p>
        <a href="#" className="breadcrumb-item" key={selectedCategory}>{selectedCategory ? selectedCategory : ""}</a>
      </div>

      <h1 className="category-h">{selectedCategory}</h1>

    </div>

  );
};





export default Navigator
