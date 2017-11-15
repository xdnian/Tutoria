// transpose the table with id selector string "theTable"
function transpose(theTable){

    var rows = $(theTable+' tr');
    var ncols = rows.eq(0).find('th,td').length;

    tem = $('<tr></tr>');
    for (cell = 0; cell < ncols; cell++) {
        next = rows.eq(cell).find('th').eq(0);
        tem.append(next);
    }
    $(theTable+' thead').append(tem);

    $(theTable+' tbody').empty();
    for (i = 1; i < ncols; i++) {
        tem = $('<tr></tr>');
        for (cell = 0; cell < ncols; cell++) {
            next = rows.eq(cell).find('th,td').eq(0);
            tem.append(next);
        }
        $(theTable+' tbody').append(tem);
    }
    $(theTable).show();
}