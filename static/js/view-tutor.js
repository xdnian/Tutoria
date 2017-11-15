$(document).ready(function () {
    //transpose the table
    transpose('table#timeslot-select');

    //clickable table cell
    $(".timeslot.available").click(function () {
        window.location = "/booking/" + $(this).attr("timeslot-id");
    });
});