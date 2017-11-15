$(document).ready(function () {
    //transpose the table
    transpose('table#offerslots');

    //clickable table cell
    $(".checkable").click(function () {
        $(this).toggleClass("bg-success");
        $(this).toggleClass("bg-dark");

        var target = $(this).find('input[type="checkbox"]');
        // If it's checked then uncheck it and vice versa
        target.prop('checked', !target.prop('checked'));
    });
});