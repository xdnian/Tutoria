$(document).ready(function () {

    var typingTimer; //timer identifier
    //on keyup, start the countdown
    $('#id_coupon').on("keydown", function () {
        clearTimeout(typingTimer);
        typingTimer = setTimeout("checkCoupon($('#id_coupon').val())", 1000);
    });
});

function checkCoupon(coupon) {
    if ($('#id_coupon').val()) {
        $.get("/checkCoupon/" + coupon, function (data, status) {
            if (data == '0') {
                $('#total').text((Number($('#rate').text()) * 1.05).toFixed(2))
                $('#commission').text((Number($('#rate').text()) * 0.05).toFixed(2))
                $('#id_coupon').addClass('is-invalid')
                $('#id_coupon').removeClass('is-valid')
            } else {
                console.log($('#rate').text())
                $('#total').text($('#rate').text())
                $('#commission').text('0.00')
                $('#id_coupon').addClass('is-valid')
                $('#id_coupon').removeClass('is-invalid')
            }
        });
    }
}