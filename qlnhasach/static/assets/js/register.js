//check

var password = document.getElementById("re_password")
  , confirm_password = document.getElementById("re_confirm_password");

function validatePassword(){
  if(password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Mật khẩu không khớp");
  } else {
    confirm_password.setCustomValidity('');
  }
}
