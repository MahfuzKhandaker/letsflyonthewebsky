// Preloader
$(window).on('load', function() { // makes sure the whole site is loaded
    $('#status').fadeOut(); // will first fade out the loading animation 
    $('#preloader').delay(350).fadeOut('slow'); // will fade out the white DIV that covers the website. 
    $('body').delay(350).css({'overflow':'visible'});
    });
  
    // jquery function
    $(document).ready(function(){
      // Fixed Header
      var offset = $('.blog-header').offset();
      checkOffset();

      $(window).scroll(function() {
        checkOffset();
      });
      function checkOffset() {
        if ($(document).scrollTop() > offset.top) {
          $('.blog-header').addClass('fixed');
        } else {
          $('.blog-header').removeClass('fixed');
        }
      }

    // markdown content image resized to bootstrap card-img-top class
    $(".card-body img").each(function(){
        $(this).addClass("card-img-top");
    });
    // reply btn fadeToggle()
    $(".comment-reply-btn").click(function(event){
        event.preventDefault();
        $(this).parent().next(".comment-reply").fadeToggle();
      });
    });