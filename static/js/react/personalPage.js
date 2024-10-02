function PP_LeftMenu ({onMenuClick}) {



  return (
    <>
      <button class = "pp-menu-bt" onClick = {()=> onMenuClick('settings')}>Настройки</button>
      <button class = "pp-menu-bt" onClick={() => onMenuClick('favorites')}>Избранное</button>
      <button class = "pp-menu-bt" onClick={() => onMenuClick('orders')}>История заказов</button>
      <button class = "pp-menu-bt" onClick={() => onMenuClick('following')}>Подписки</button>
      <button class = "pp-menu-bt exit-bt" onClick={() => onMenuClick('exit')}>Выйти из аккаунта</button>
    </>
  );
}

function PP_Content ({activeMenu}) {
  const renderContent = () => {
    switch (activeMenu){
      case 'settings':
        return <div class="h-pp-content">Настройки профиля</div>;
      case 'favorites':
        return <div class="h-pp-content">Избранное</div>;
      case 'orders':
         return <div class="h-pp-content">История заказов</div>;
      case 'following':
        return <div class="h-pp-content">Ваши подписки</div>;
      default:
        return <div class ="h-pp-content">Выберите пункт в меню</div>;
    }

  };

  return (
      <>
        {renderContent ()}
      </>


  );

}
function PersonalPage () {
  // получение состояния
  const [activeMenu, setActiveMenu] = React.useState('settings');

  // обработчик  клика \ он меняет состояние при клике на кнопку меню
  const MenuClick = (menuItem) => {
    setActiveMenu(menuItem);
  };

  return (
    <>
      {/* Рендерим левое меню */}
      <div id="pp-menu" class="mb-leftside-sizing mb-pesonalMenu b-shadow">
        <PP_LeftMenu onMenuClick={MenuClick} />
      </div>

      {/* Рендерим контент в правом блоке */}
      <div id="pp-menu-content" class="mb-rightside-sizing mb-pesonalMenuContent">
        <PP_Content activeMenu={activeMenu} />
      </div>
    </>
  );

}





ReactDOM.render(<PersonalPage />, document.getElementById('mainblock'))
// ReactDOM.render(<PersonalPage />, document.getElementById('pp-menu'));
// ReactDOM.render(<PersonalPage />, document.getElementById('pp-menu-content'));

// PersonalPage ();
