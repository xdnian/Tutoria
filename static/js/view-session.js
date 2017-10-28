var status_badge = {
    "booked":'<h6 class="card-subtitle mb-2 text-muted"><span class="badge badge-info">Booked</span></h6>',
    "committed": '<h6 class="card-subtitle mb-2 text-muted"><span class="badge badge-warning">Committed</span></h6>',
    "finished": '<h6 class="card-subtitle mb-2 text-muted"><span class="badge badge-dark">Finished</span></h6>',
    "canceled": '<h6 class="card-subtitle mb-2 text-muted"><span class="badge badge-danger">Canceled</span></h6>'
};

$(document).ready(function(){
    (function(){
        $(".card-title").after(status_badge[$(this).attr("status")]);
    }());

    $(".session-cancel-btn").click(function(){
        window.location = "/canceling/"+$(this).parent().attr("sessionId");
    });
});