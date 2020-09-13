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
    // like button
    $("#like").click(function(event){
      event.preventDefault();
      console.log($("#like").val())
      console.log("from jquery section")
      var pk = $(this).attr('value');
      $.ajax({
        type : "POST",
        url : '{% url "post_likes" %}',
        data : {'id': pk, "csrfmiddlewaretoken": '{{ csrf_token }}'},
        dataType : 'json',
        success : function(response){
          $('#like-section').html(response['form'])
          console.log($('#like-section').html(response['form']));
        },
        error : function(rs, e){
          console.log(rs.responseText);
        }

      });

    });
    // $('.likebutton').click(function(){ 
    //   var id; 
    //   id = $(this).attr("data-catid"); 
    //   $.ajax( 
    //   { 
    //       type:"POST", 
    //       url: "{% url 'post_likes' %}", 
    //       data:{ 
    //                post_id: id 
    //   }, 
    //   success: function( data ) 
    //   { 
    //       $( '#like'+ id ).removeClass('btn btn-primary btn-lg'); 
    //       $( '#like'+ id ).addClass('btn btn-success btn-lg'); } }) });
});