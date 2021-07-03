$(document).ready(function(){
   
    var add_image_link = document.getElementById('add-new-image-link');
    var add_image_form = document.getElementById('add-image-container');
    add_image_link.addEventListener('click',function(){

        if(add_image_form.classList.contains('d-none') ){
            add_image_form.classList.remove('d-none');
            add_image_form.classList.add('d-flex');
            add_image_link.innerHTML = 'Close';
        } else {
            
            add_image_form.classList.remove('d-flex');
            add_image_form.classList.add('d-none');
            add_image_link.innerHTML = 'Add a new image';
        };
        
    });
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