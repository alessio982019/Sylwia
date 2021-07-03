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


// (function () {
//     var body = document.body,
//             e = document.documentElement,
//             scrollPercent;
//     $(window).unbind("scroll").scroll(function () {
//         scrollPercent = 100 * $(window).scrollTop() / ($(document).height() - $(window).height()) + 5;
//         body.style.backgroundPosition = "0px " + scrollPercent + "%";
//     });
// })();
var window_top = $(window).scrollTop();
    
$(window).scroll(function() {    
    var scroll = $(window).scrollTop();
    
    var objectSelect = $("#background-logo");
    var objectPosition = objectSelect.offset().top - 50 ;
    var objectPosition_btm = objectPosition + objectSelect.height() + 25;
    var nav = document.getElementById('container-nav');
    var a = document.getElementById('container-nav').getElementsByTagName('a');
    var drop_menu = document.getElementById('dropdown-menu');
    var navbar = document.getElementById('navbar-home');
    var contact_box = $('#contact');
    var contact_top = contact_box.offset().top - 50;
    var contact_btm= contact_top + contact_box.height() +50;
    

    if (scroll > objectPosition & scroll < objectPosition_btm) {
     console.log("FIrst");
        navbar.classList.remove('navbar-dark');
        navbar.classList.add('navbar-light');

        for( i = 0; i < a.length;i++){

            a[i].classList.add('text-dark');
            a[i].classList.remove('text-light');
        }

    } else if(scroll > objectPosition_btm & scroll < objectPosition){
        console.log("Second");
        navbar.classList.add('navbar-dark');
        navbar.classList.remove('navbar-light');

    }  
    else if (scroll > contact_top & scroll <     contact_btm ) {
        navbar.classList.remove('navbar-dark');
        navbar.classList.add('navbar-light'); 
        for( i = 0; i < a.length;i++){

            a[i].classList.add('text-dark');
            a[i].classList.remove('text-light');
        }

    }
    
    else {
        console.log("Third");
        navbar.classList.add('navbar-dark');
        navbar.classList.remove('navbar-light');

        for( i = 0; i < a.length;i++){

            a[i].classList.remove('text-dark');
            a[i].classList.add('text-light');
        }
        
    }
});
$(document).ready(function () {
    var $horizontal = $('#img-home');
    var startPosition = $horizontal.position().left;
    var speed = 14;
    $(window).scroll(function () {
        var st = $(this).scrollTop();
        var newPos = (st * (speed/100)) + startPosition;
        $horizontal.css({
            'left': newPos
        });
    });
});