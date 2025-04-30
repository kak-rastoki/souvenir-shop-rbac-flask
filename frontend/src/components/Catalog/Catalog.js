import React, {useState, useEffect} from 'react';
import './Catalog.css';
import ProductCard from '../ProductCard/ProductCard';
import Navigator  from '../Navigator/Navigator';
import Filters from '../Filters/Filters';



function Catalog(){

  const [products,setProducts] = useState([]);




  const handleCategoryChange = (newProducts) => {
    setProducts(newProducts);
    console.log(newProducts)
  };



  return (
    <div className="catalog-page">
        <Navigator categoryChange = {handleCategoryChange}/>
        <div className ="container">
          <Filters />
          <div className="product-grid">
            {products.map(product => (
                <ProductCard key={product.id} product={product} />
            ))}
        </div>
        </div>
    </div>
  );

}




export default Catalog;
