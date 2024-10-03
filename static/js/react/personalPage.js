function PP_LeftMenu ({onMenuClick}) {



  return (
    <>

      <button class = "pp-menu-bt" onClick = {()=> onMenuClick('settings')}><i class="fa fa-address-card" aria-hidden="true"></i> Настройки</button>
      <button class = "pp-menu-bt" onClick={() => onMenuClick('favorites')}><i class="fa fa-heart" aria-hidden="true"></i> Избранное</button>
      <button class = "pp-menu-bt" onClick={() => onMenuClick('orders')}><i class="fa fa-history" aria-hidden="true"></i> История заказов</button>
      <button class = "pp-menu-bt" onClick={() => onMenuClick('following')}><i class="fa fa-user-circle" aria-hidden="true"></i> Подписки</button>
      <button class = "pp-menu-bt exit-bt" onClick={() => onMenuClick('exit')}><i class="fa fa-sign-out" aria-hidden="true"></i> Выйти из аккаунтa</button>
    </>
  );
}

function PP_Content ({activeMenu}) {
  const renderContent = () => {
    switch (activeMenu){
      case 'settings':
        return <div class="h-pp-content"><i class="fa fa-address-card" aria-hidden="true"></i> Настройки профиля</div>;
      case 'favorites':
        return <div class="h-pp-content"><i class="fa fa-heart" aria-hidden="true"></i> Избранное</div>;
      case 'orders':
         return <div class="h-pp-content"><i class="fa fa-history" aria-hidden="true"></i> История заказов</div>;
      case 'following':
        return <div class="h-pp-content"><i class="fa fa-user-circle" aria-hidden="true"></i> Ваши подписки</div>;
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

function Settings () {


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
