$('#chat-form').on('submit', function(event){
    event.preventDefault();

    $.ajax({
        url : '/post/',
        type : 'POST',
        data : { msgbox : $('#chat-msg').val(), 
                 receiver_name : $('#receiver').val()},

        success : function(json){
            $('#chat-msg').val('');
            $('#msg-list').prepend('<div class="row justify-content-end"><div class="col-md-7"><div class="alert alert-light"><p>' + json.msg + '</p><div class="time">Just now</div></div></div></div>');

        }
    });
});

function getMessages(){
    if (!scrolling) {
        var URL = window.location.href;
        URL = URL.split("/");
        receiver = URL[URL.length-2];
        var func_url = '/messages/'.concat(receiver);
        $.get(func_url, function(messages){
            $('#msg-list').html(messages);
        });
    }
    scrolling = false;
}

var scrolling = false;
$(function(){
    refreshTimer = setInterval(getMessages, 2000);
});

$(document).ready(function() {
     $('#send').attr('disabled','disabled');
     $('#chat-msg').keyup(function() {
        if($(this).val() != '') {
           $('#send').removeAttr('disabled');
        }
        else {
        $('#send').attr('disabled','disabled');
        }
     });
 });

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});