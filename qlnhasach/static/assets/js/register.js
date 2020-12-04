//check

var password = document.getElementById("re_password")
  , confirm_password = document.getElementById("re_confirm_password")
    ,today=new Date().toISOString().split('T')[0]
    ,date= document.getElementById("re_date").toISOString().split('T')[0];

function validatePassword(){
  if(password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Mật khẩu không khớp");
  } else {
    confirm_password.setCustomValidity('');
  }
}

function validateDate(){
    if(date.value() > today.value()){
        date.setCustomValidity("Ngày sinh không hợp lệ");
    }
    else
        date.setCustomValidity("");
}
password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;
date.onchange= validateDate()
