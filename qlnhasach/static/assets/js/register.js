
var password = document.getElementById("re_password")
  , confirm_password = document.getElementById("re_confirm_password");

function validatePassword(){
  if(password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Mật khẩu không khớp");
  } else {
    confirm_password.setCustomValidity('');
  }
}

/*animation*/
function addcart(){

    var button = $('#addtocart');
    var cart = $('#cart');
    var cartTotal = cart.attr('data-totalitems');
    var newCartTotal = parseInt(cartTotal) + 1;

    button.addClass('sendtocart');

    setTimeout(function(){
      button.removeClass('sendtocart');
      cart.addClass('shake').attr('data-totalitems', newCartTotal);
      setTimeout(function(){
        cart.removeClass('shake');
      },500)
    },1000)

}
function addToCart(id, ten_sach, don_gia) {
    fetch('/api/cart', {
        method: 'POST',
        body: JSON.stringify({
            "id": id,
            "ten_sach": ten_sach,
            "don_gia": don_gia
        }),
        headers: {
            "Content-Type": 'application/json'
        }
    }).then(res => res.json()).then(data => {
        var cart = document.getElementById('cart-info');
        cart.innerText = `${data.total_quantity} - ${data.total_amount} VNĐ`
    })
}

function page_trans(){
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
