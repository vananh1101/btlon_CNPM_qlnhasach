
/*animation*/
function addcart(){

    var button = $('.addtocart');
    var cart = $('#cart');
    var cartTotal = cart.attr('data-totalitems');
    var newCartTotal = parseInt(cartTotal) + 1;

    setTimeout(function(){
      cart.addClass('shake').attr('data-totalitems', newCartTotal);
      setTimeout(function(){
        cart.removeClass('shake');
      },100)
    },500)

}
function addToCart(productId, productName, price) {
    fetch('/api/cart', {
        method: 'POST',
        body: JSON.stringify({
            "id": productId,
            "ten_sach": productName,
            "don_gia": price
        }),
        headers: {
            "Content-Type": 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data)
    })
}

function page_trans(path){
    window.location="http://127.0.0.1:4000/login"
}
$(function (){
  var star = '.fa-stars',
      selected = '.selected';

  $(star).on('click', function(){
    $(selected).each(function(){
      $(this).removeClass('selected');
    });
    $(this).addClass('selected');
  });

});


function pay() {
    fetch('/payment', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json'
        }
    }).then(res => res.json()).then(data => {
        alert(data.message);
    }).catch(res => {
        console.log(res);
    })
}
$(function (){
  var star = '.fa-star',
      selected = '.selected';

  $(star).on('click', function(){
    $(selected).each(function(){
      $(this).removeClass('selected');
    });
    $(this).addClass('selected');
  });

});

