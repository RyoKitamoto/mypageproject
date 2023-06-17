(()=>{
window.onload=function(){

console.log('script.jsを読み込んでいます。');

// モーダルを表示(idをつかってるため複数モーダルを実装したい今回はキャンセルで)
// const buttonOpen = document.getElementById('modalOpen');
// // const buttonOpen = document.querySelector('modalOpen');
// const modal = document.getElementById('easyModal');
// const buttonClose = document.getElementsByClassName('modalClose')[0];


// console.log(buttonOpen);
// buttonOpen.addEventListener('click',function(){
//     modal.style.display = 'block';
// });



// buttonClose.addEventListener('click',function(){
//     modal.style.display = 'none';
// });
// // モーダルコンテンツ以外がクリックされた時
// addEventListener('click', outsideClose);
// function outsideClose(e) {
//   if (e.target == modal) {
//     modal.style.display = 'none';
//   }
// }

// お試しモーダル（data属性を持たせて複数モーダルを表示できるようにした）
const modalBtns = document.querySelectorAll(".modalOpen");
modalBtns.forEach(function (btn) {
  btn.onclick = function () {
    var modal = btn.getAttribute('data-modal');
    document.getElementById(modal).style.display = "block";
  };
});
const closeBtns = document.querySelectorAll(".modalClose");
closeBtns.forEach(function (btn) {
  btn.onclick = function () {
    var modal = btn.closest('.modal');
    modal.style.display = "none";
  };
});

window.onclick = function (event) {
  if (event.target.className === "modal") {
    event.target.style.display = "none";
  }
};





}


})();
