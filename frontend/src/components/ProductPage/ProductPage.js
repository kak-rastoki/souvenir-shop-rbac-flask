import React, {useState, useEffect} from "react";
import './ProductPage.css';
import { useParams } from 'react-router-dom';
import { Link } from 'react-router-dom';



function ProductPage() {
    const {id} = useParams(); // параметр id передастся через строку url
    const [product, setProduct] = useState (null);
    const [loading,setLoading] = useState (true);
    const [error,setError] = useState (false);

    const fetchProduct = () => {
        // let hasFetched = false;
        // if (hasFetched) return; // Если запрос уже выполнен, выходим
        // hasFetched = true;
        if (!id) {
            setError('Ошибка передачи ID товара');
            setLoading(false);
            setProduct(null);
            console.log (error);
            return;
        };

        //ЗАПРОС продукта по id
        const url = new URL (`http://localhost:5000/api/product/${id}`);
        fetch (url)
        .then(respone => {
            if (!respone.ok) {
                return respone.json()
                .then(err=> {throw new Error(err.error || 'Ошибка сети или сервера')});
                }
            return respone.json()
        })
        .then (data => {

            setProduct(data || null);
            console.log('Полученные данные товара', data);
            setLoading(false);
        })
        .catch(err=>{
            setError(`Ошибка при загрузки товара ${id} с сервера`);
            setLoading (false);
            console.log(error)
        });

    };







    useEffect(()=> {
        fetchProduct()
    },[id]);

     //ЗАГРУЗКА
    if (loading) {
        return <p>Подождите, идет загрузка товара...</p>
    };
    if (error) {
        return <p>Произошла ошибка: {error}.</p>
    };
    if (!product) return <div>Товар не найден</div>;



  return (

    <div className="productPage-wrapper">
        <div className="flex-group">
            <div className="breadcrumbs">
                <span>Магазин "Студенческий" </span>
                &gt; <span><Link to={`/`}>Категории</Link></span> &gt;

                <span> Сувениры </span> &gt;
                <span> {product.name} </span>
            </div>

            <Link to={`/`}  className="link"><button>Вернуться в каталог</button></Link>

        </div>
        <div className="productPage-card">
            <div className="product-image">
                <img src={`data:image/jpeg;base64,${product.image}`} width="360px"/>
                <div className="thumbnails">
                    <div className="thumbnail"></div>
                    <div className="thumbnail"></div>
                    <div className="thumbnail"></div>
                    <div className="thumbnail"></div>
                </div>
            </div>
            <div className="product-content">
                <h1>{product.name}</h1>

                <div className="product-discription">
                    <font color='#828282'>Описание товара ☟ </font>
                    <p>{product.discription}</p>
                </div>
                <div className="flex-group cost-button-container">
                    <p className="cost">{product.cost}₽</p>
                    <button>В коризину</button>
                </div>
                <div className="flex-group option-block">
                    <div className="flex-group option"><p>Артикул:</p><div className="tag"><p>12A34</p></div></div>
                    <div className="flex-group option"><p>Категория:</p><div className="tag"><p>{product.category}</p></div></div>
                    <div className="flex-group option"><p>Мастер:</p><div className="tag"><p>{product.master}</p></div></div>
                </div>




            </div>
        </div>
    </div>
  )
};

export default ProductPage;
