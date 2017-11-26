var status_badge = {
    "Booked":'<h6 class="card-subtitle mb-2 text-muted"><span class="badge badge-info">Booked</span></h6>',
    "Pending": '<h6 class="card-subtitle mb-2 text-muted"><span class="badge badge-warning">Pending</span></h6>',
    "Committed": '<h6 class="card-subtitle mb-2 text-muted"><span class="badge badge-success">Committed</span></h6>',
    "Canceled": '<h6 class="card-subtitle mb-2 text-muted"><span class="badge badge-danger">Canceled</span></h6>',
    "Ended": '<h6 class="card-subtitle mb-2 text-muted"><span class="badge badge-dark">Ended</span></h6>',
    "Reviewed": '<h6 class="card-subtitle mb-2 text-muted"><span class="badge badge-dark">Reviewed</span></h6>'
};

$(document).ready(function(){
    $(".card-title").each(function(){
        $(this).after(status_badge[$(this).attr("status")]);
    });
    
    // $(".session-cancel-btn").click(function(){
    //     window.location = "/canceling/"+$(this).parent().attr("sessionId");
    // });
});