function onClickVisible(category_div){
    var ref_div = category_div.getAttribute('reference_div');
    var ref_pic = document.getElementById(ref_div);
    ref_pic.classList.remove('d-none');
    ref_pic.scrollIntoView();
    console.log(ref_div);

};

function onClickNotVisible(category_div){
    var ref_div = category_div.getAttribute('reference_div');
    var ref_pic = document.getElementById(ref_div);
    ref_pic.classList.add('d-none');
    console.log(ref_div);

};
var window_top = $(window).scrollTop();
    
// $(window).scroll(function() {    
//     var scroll = $(window).scrollTop();
    
//     var objectSelect = $("#about");
//     var objectPosition = objectSelect.offset().top;
//     console.log(scroll + "  " + objectPosition)
//     var home_div = document.getElementById("home");
//     if (scroll > objectPosition) {
//         console.log("change");
        
//         home_div.classList.add("position-absolute");
//     } else {
//         home_div.classList.remove("position-absolute");
//     }
// });
$(document).ready(function(){
   
    // if (window_top > div_top) {
    //     document.getElementById('home').classList.remove('position-absolute')


    //     } 
    //     //if window top reaches the limit removed class
    //     if(window_top < document.getElementById('about').position().top){

    //         document.getElementById('home').classList.add('position-absolute')
    //     }

    var category_div = document.getElementsByClassName("category-pic");

    for (var i = 0; i < category_div.length;i+=1){
        (function(){
            var element_div = category_div[i];

            element_div.addEventListener("click",function(){ onClickVisible(element_div) });
        }());
            
          
    };

    var close_div = document.getElementsByClassName("close-gallery");

    for (var i = 0; i < close_div.length;i+=1){
        (function(){
            var close_btn = close_div[i];

            close_btn.addEventListener("click",function(){ onClickNotVisible(close_btn) });
        }());
            
          
    }


 
})