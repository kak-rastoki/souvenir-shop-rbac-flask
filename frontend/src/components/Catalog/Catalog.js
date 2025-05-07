import React, { useState, useEffect, useCallback } from 'react';
import './Catalog.css';
import ProductCard from '../ProductCard/ProductCard';
import Navigator from '../Navigator/Navigator';
import Filters from '../Filters/Filters';


function Catalog() {
  const perPage =12;
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [selectedCategory, setSelectedCategory] = useState('Новинки');
  const [priceFilter,setPriceFilter] = useState ({minPrice:'',maxPrice:''});




  const handleCategoryChange = useCallback((category,minPrice='',maxPrice='') => {
    if (!category) {
      setError('Категория не выбрана');
      setLoading(false);
      setProducts([]);
      return;
    }

    const url = new URL("http://localhost:5000/api/products_by_category");

    if (selectedCategory !== category) {
      setCurrentPage(1);
    }
    setSelectedCategory(category);

    setLoading(true);
    setError(null);

    if (currentPage) url.searchParams.append ('page',currentPage);
    if (perPage) url.searchParams.append ('per_page',perPage);

    fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        category: category,
        priceFilter: {minPrice:priceFilter.minPrice, maxPrice:priceFilter.maxPrice},
      }),
    })
      .then(response => {
        if (!response.ok) {
          return response.json().then(err => {
            throw new Error(err.error || 'Ошибка сети или сервера');
          });
        }
        return response.json();
      })
      .then(data => {
        console.log('Полученные данные:', data);
        setProducts(data.products || []);
        setTotalPages(data.total_pages || 1);
        setCurrentPage(data.current_page || 1);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message || 'Ошибка при загрузке данных');
        setLoading(false);
        setProducts([]);
        console.error('Error:', err);
      });
  },[selectedCategory,currentPage,perPage,priceFilter.maxPrice,priceFilter.minPrice]);

  // Обнволение товаров при изменении текущей старницы
  useEffect(() => {
    handleCategoryChange(selectedCategory);
  }, [currentPage, selectedCategory, priceFilter.minPrice, priceFilter.maxPrice]);


  const handlePriceFilterChange = (minPrice,maxPrice) => {
    setPriceFilter ({minPrice,maxPrice});
    setCurrentPage (1);
    handleCategoryChange(selectedCategory);
  }



  return (
    <div className="catalog-page">
      <Navigator categoryChange={handleCategoryChange} />
      <div className="container">
        <Filters priceFilterChange = {handlePriceFilterChange} />
        <div className='container-grid'>
          <div className="product-grid">
            {loading ? (
              <div className="load-block">
                <div className="loader"></div>
                <div className="loader"></div>
                <div className="loader"></div>
                <div className="loader"></div>
                <div className="loader-shadow"></div>
                <p>Подождите, идет загрузка товаров...</p>
              </div>
            ) : error ? (
              <p className="error-message">{error}</p>
            ) : products.length === 0 ? (
              <p>Товары не найдены</p>
            ) : (
              products.map((product,index) => (
                <ProductCard key={product.id} product={product} animationDelay={index * 0.08}/>
              ))
            )}
          </div>
          {!loading && products.length >0 && (
            <div className="pagination-controls">
              <div className='buttons-wrapper'>
                <button
                  onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                  disabled={currentPage === 1}
                >
                  ← Предыдущая страница
                </button>
                <button
                  onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                  disabled={currentPage === totalPages}
                >
                  Следующая страница →
                </button>
                <button
                  onClick={() => setCurrentPage(totalPages)}
                  disabled={currentPage === totalPages}
                >
                  Последняя📑
                </button>
              </div>
              <span>Страница {currentPage} из {totalPages}</span>
            </div>
        )}
        </div>
      </div>
    </div>
  );
}

export default Catalog;
