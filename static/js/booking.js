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
                $('#total').val($('#rate').val())
                $('#commission').val('0')
                $('#id_coupon').addClass('is-invalid')
                $('#id_coupon').removeClass('is-valid')
            } else {
                $('#total').val(Number($('#rate').val()) * 1.05)
                $('#commission').val(Number($('#rate').val()) * 0.05)
                $('#id_coupon').addClass('is-valid')
                $('#id_coupon').removeClass('is-invalid')
            }
        });
    }
}