let tab = document.querySelector(".reg-wrap"); // оболочкая окна регистрации и логина
// let tabs = tab.querySelector(".reg-container"); // по приколу
let tabHeader = tab.querySelector('.rg-tabs'); // верхний хедер окна со вкладками
let tabHeaderElements = tabHeader.querySelectorAll (".rg-tabs > div"); // Все вклдаки собствено
let tabBody = tab.querySelector(".rg-tabBody"); // тело вкладок
let tabBodyElements = tab.querySelectorAll(".rg-tabBody > div"); // непосредственно поля
console.log (tabHeader,tabHeaderElements, "я не понимаю че не раблтает")

for(let i=0; i<tabHeaderElements.length; i++){
  tabHeaderElements[i].addEventListener("click", function(){
    tabHeader.querySelector(".active").classList.remove("active");
    tabHeaderElements[i].classList.add("active");
    tabBody.querySelector(".active").classList.remove("active");
    tabBodyElements[i].classList.add("active");
  });

}
