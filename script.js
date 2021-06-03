
   

var nav_link = document.getElementsByClassName("nav-link");

var scroll_body = function(){
    var div_id = this.getAttribute("content_id");
    alert("Hello!");
    // window.scrollTo(0, 0);
    // $('html, body').animate({
    //     scrollTop: $(hash).offset().top
    // }, 400, function(){
        
    //     window.location.hash = hash;
    // });
    
    
}
for ( var i = 0; i < nav_link.length; i++){

    nav_link[i].addEventListener("click",scroll_body,false);


}
$('document').ready(function(){
    document.getElementById("scroll-services").addEventListener('click',function(){
        document.getElementById('div-services').scrollIntoView();

});

$(window).scroll(function() {    
    var scroll = $(window).scrollTop();
    var objectSelect = $("#div-home-picture");
    var home_div = document.getElementById('div-home-picture');
    let height = home_div.offsetHeight;
    var links = document.getElementsByClassName('nav-link');

    for ( i = 1;i < links.length;i++){
        if (scroll > height - 150) {
            
            // $("#navbar").addClass("bg-dark");
            $("#navbar").addClass("fixed-nav");
            
        } else {
           
            // $("#navbar").removeClass("bg-dark");
            $("#navbar").removeClass("fixed-nav");
        }

    }
    
    
        
        

});


});
       


