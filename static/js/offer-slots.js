$(document).ready(function () {
    //transpose the table
    var rows = $('table#offerslots tr');
    var ncols = rows.eq(0).find('th,td').length;

    tem = $('<tr></tr>');
    for (cell = 0; cell < ncols; cell++) {
        next = rows.eq(cell).find('th').eq(0);
        tem.append(next);
    }
    $('table#offerslots thead').append(tem);

    $('table#offerslots tbody').empty();
    for (i = 1; i < ncols; i++) {
        tem = $('<tr></tr>');
        for (cell = 0; cell < ncols; cell++) {
            next = rows.eq(cell).find('th,td').eq(0);
            tem.append(next);
        }
        $('table#offerslots tbody').append(tem);
    }
    $('table#offerslots').show();

    //clickable table cell
    $(".checkable").click(function () {
        $(this).toggleClass("bg-success")
        $(this).toggleClass("bg-dark")

        var target = $(this).find('input[type="checkbox"]');
        // If it's checked then uncheck it and vice versa
        target.prop('checked', !target.prop('checked'));
    });
});