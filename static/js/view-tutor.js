$(document).ready(function () {
    //transpose the table
    transpose('table#timeslot-select');

    //clickable table cell
    $(".tutor-info").click(function () {
        window.location = "/viewTutor/" + $(this).attr("tutor-id");
    });
});