$(document).ready(function() {
  if($(window).width() < 1000){
    $("#sidebar").mmenu({
      navbar: {
        add: false,
      },
      dragOpen: true,
      dragClose: true,
      offCanvas: {
        zposition: 'front',
      },
    });
    var api = $("#sidebar").data("mmenu");
  }
  var path = window.location.pathname;
  $('.nav .item a[href="'+path+'"]').parents('.item').addClass('active');
});
