import React, {useState, useEffect} from 'react';
import './Catalog.css';
import ProductCard from '../ProductCard/ProductCard';
import Navigator  from '../Navigator/Navigator';
import Filters from '../Filters/Filters';



function Catalog(){

  const [products,setProducts] = useState([]);
  const [error,setError] = useState(false);
  const [loading,setLoading] = useState(null);


  useEffect(()=> {
    async function fetchProducts() {
      try{
        const response = await fetch ('http://localhost:5000/api/products');

        if (!response.ok) {
          throw new Error('HTTP ошибочка со статусом: ${response.status}');
        }

        const data = await response.json();
        setProducts(data);

      }catch(error){
        setError(error);
        console.error("Ошибка при загрузке товаров:", error);
      }finally {
        setLoading(false)
      }

    }

    fetchProducts();
  }, []);

  if (loading) {
    return  <p>Загразка каталога. Подождите...</p>;
  }

  if (error){
    return <p>Упс. Ошибка загрзуки: {error.message}</p>;
  }


  return (
    <div className="catalog-page">
        <Navigator />
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
