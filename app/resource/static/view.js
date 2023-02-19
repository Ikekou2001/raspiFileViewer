// 画像のmax縦幅
var modHeight = "calc(100vh - " + document.getElementById("header").clientHeight + "px)";
// ナビゲーションバーの取得
var navbarDropdown = document.getElementById("navbarDropdown");
// アクティブドロップダウン
var activeDropdownItem = null;
document.querySelectorAll(".dropdown-item").forEach(function(target){
  if (target.classList.contains("active") && activeDropdownItem == null){
    activeDropdownItem = target;
  }
  target.addEventListener("click", function(e){
    navbarDropdown.textContent = target.textContent;
    activeDropdownItem.classList.remove("active");
    activeDropdownItem = target;
    activeDropdownItem.classList.add("active");
  });
});
// カルーセルの取得
var imgCarousel = document.getElementById("imgCarousel");
imgCarousel.addEventListener("slide.bs.carousel", function(e){
  navbarDropdown.textContent = e.to + 1;
  activeDropdownItem.classList.remove("active");
  activeDropdownItem = document.querySelector(".dropdown-item#d" + e.to);
  activeDropdownItem.classList.add("active");
  location.hash = e.to + 1;
});
// 各画像にクリックイベントを追加
document.querySelectorAll("img.img-content").forEach(function(target){
  target.addEventListener("click", function(e){
    var activeCarousel = new bootstrap.Carousel(imgCarousel, {});
    activeCarousel.next();
  });
  target.style.maxHeight = modHeight;
});
// 遅延読込
lazyload();
// カルーセルの初期位置
var tmpCarousel = new bootstrap.Carousel(imgCarousel, {});
var tmpURL = new URL(document.URL);
var p = parseInt(tmpURL.hash.replace("#", ""));
if(!isNaN(p)){
  tmpCarousel.to(p - 1);
}