$(document).ready(function () {
    $(".tutor-info").click(function () {
        window.location = "/viewTutor/" + $(this).attr("tutor-id");
    });
    $("#tutor-table").tablesorter({ 
        headers: { 
            0: { sorter: false }, 
            4: { sorter: false }
        } //disable third colomn for sorting
    }); 
});