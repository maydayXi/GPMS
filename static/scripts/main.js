// $(window).load(function() {
//     $("#preloader").fadeOut("slow");
// });

$(document).ready(function(){


     new WOW().init();


     $('#top-nav').onePageNav({
        currentClass: 'current',
        changeHash: true,
        scrollSpeed: 1200
    });


    //animated header class
    $(window).scroll(function() {
    var scroll = $(window).scrollTop();
    //console.log(scroll);
    if (scroll > 200) {
        console.log('add');
        $(".navbar").addClass("animated");
    } else {
        console.log('remove');
        $(".navbar").removeClass("animated");
    }});



    /*$('input, textarea').data('holder', $('input, textarea').attr('placeholder'));

    $('input, textarea').focusin(function () {
        $(this).attr('placeholder', '');
    });
    $('input, textarea').focusout(function () {
        $(this).attr('placeholder', $(this).data('holder'));
    });*/




});
