$(window).on("load",function(){
    $(".loader-wrapper").delay(200).fadeOut("slow");
    $(".loader-wrapper").promise().done(function(){
        $(".contentContainer").show();
    })
});