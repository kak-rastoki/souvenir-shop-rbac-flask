import React, {useState, useEffect} from 'react';
import './Catalog.css';
import ProductCard from '../ProductCard/ProductCard';
import Navigator  from '../Navigator/Navigator';
import Filters from '../Filters/Filters';



function Catalog(){

  const [products,setProducts] = useState([]);
  const [loading,setLoading] = useState (true);
  const [error,setError] = useState (null);



  const handleCategoryChange = (newProducts,newLoading,newError) => {
    setLoading (newLoading);
    setError(newError);
    setProducts(newProducts);
    console.log(newProducts)
  };



  return (
    <div className="catalog-page">
        <Navigator categoryChange = {handleCategoryChange}/>
        <div className ="container">
          <Filters />
          <div className="product-grid">
            {loading ? <p>Подождите, идет загрузка товаров...</p> : null}
            {error ? <p>{error}</p> : null}
            {products.map(product => (
                <ProductCard key={product.id} product={product} />
            ))}
        </div>
        </div>
    </div>
  );

}




export default Catalog;
