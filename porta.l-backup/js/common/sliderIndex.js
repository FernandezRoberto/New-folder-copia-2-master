jQuery(function($) {
  //#main-slider
  $(function(){
    $('#main-slider.carousel').carousel({
      interval: 8000
    });
  });
  //Initiat WOW JS
  new WOW().init();
  $(window).scroll(function(){
    if ($(this).scrollTop() > 100) {
      $('.scrollup').fadeIn();
    } else {
      $('.scrollup').fadeOut();
    }
  });
  $('.scrollup').click(function(){
    $("html, body").animate({ scrollTop: 0 }, 1000);
    return false;
  });
});