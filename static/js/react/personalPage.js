function pp_MenuPositing () {
  const [activeMenu, setActiveMenu] = React.useState('settings');

  const MenuClick = (menuItem) => {
    setActiveMenu(menuItem);
  };


  const renderContent = () => {
    switch (activeMenu){
      case 'settings':
        return <div>Настройки</div>;
      case 'favorites':
        return <div>Избранное</div>;
      case 'orders':
         return <div>История заказов</div>;
      default:
        return <div>Выберите пункт в меню</div>;
    }

  };

  return (
    <div>
      {/* блок меню */}

      <div>
        <button onClick = {()=> MenuClick('settings')}>Настройки</button>
        <button onClick={() => MenuClick('favorites')}>Избранное</button>
        <button onClick={() => MenuClick('orders')}>История заказов</button>
      </div>

      <div>
        {renderContent ()}
      </div>
    </div>

  );

}

ReactDOM.render(<pp_MenuPositing />, document.getElementById('pp-menu'));
ReactDOM.render(<PersonalPage />, document.getElementById('pp-menu-content'));
