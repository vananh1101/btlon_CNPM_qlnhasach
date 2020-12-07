const stars = document.querySelectorAll('.star');
const output = document.querySelectorAll('.output');

for(x = 0; x < stars.length; x++){
    stars[x].starValue = (x+1);

    ["click", "mouseover", "mouseout"].forEach(function(e){
        stars[x].addEventListener(e,showRating);
    })
}

function showRating(e){
    let type = e.type;
    console.log(type);
}