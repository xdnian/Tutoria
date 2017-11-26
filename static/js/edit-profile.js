$(document).ready(function () {
    $("#edit-profile-btn").click(function () {
        $("#profile-form td>:first-child").toggleClass("form-control-plaintext");
        $("#profile-form td>:first-child").toggleClass("form-control");
        $("#profile-form td>select").toggleAttr("disabled");
        $("#profile-form td>input").toggleAttr("readonly");
        $("#profile-form td>textarea").toggleAttr("readonly");
        $(".help-text").toggle();
        $("#save-profile-btn").toggle();
        if ($(this).text() == "Edit") {
            $(this).text("Cancel");
        } else {
            $(this).text("Edit");
        }
    });

    $("#id_tutortype").change(function () {
        if ($(this).val() == "C") {
            $("#id_price").val(0.00);
            $("#id_price").attr("readonly","");
        } else {
            $("#id_price").removeAttr("readonly");
        }
    });
});

jQuery.fn.toggleAttr = function (attr) {
    return this.each(function () {
        var $this = $(this);
        $this.attr(attr) ? $this.removeAttr(attr) : $this.attr(attr, attr);
    });
};