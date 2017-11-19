$(document).ready(function () {
    //transpose the table
    transpose('table#timeslot-select');

    //clickable table cell
    $(".timeslot.available").click(function () {
        window.location = "/booking/" + $(this).attr("timeslot-id");
    });

    $("#showTimeslotBtn").click(function() {
        $('html, body').delay(200).animate({
            scrollTop: $("#showTimeslotBtn").offset().top
        }, 600);
    });
});