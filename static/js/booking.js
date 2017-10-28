$(document).ready(function(){
    $(".tutor-info").click(function(){
        window.location = "/booking/"+$(this).attr("tutor-id");
    });
});