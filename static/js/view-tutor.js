$(document).ready(function () {
    //transpose the table
    transpose('table#timeslot-select');

    //clickable table cell
    $(".timeslot.available").click(function () {
        window.location = "/booking/" + $(this).attr("timeslot-id");
    });

    $("#showTimeslotBtn").click(function () {
        $('html, body').delay(200).animate({
            scrollTop: $("#showTimeslotBtn").offset().top
        }, 600);
    });

    $('#show-all-review').click(function () {
        if ($('#review-list').html()) {
            $('#review-list').html('')
        } else {
            $.getJSON('/getAllReviewFormatted/' + $(this).attr('tutorid'), function (data, status) {

                reviews = data.reviews;

                reviews_html = '';
                i = 0;
                for (r in reviews) {
                    if (i == 0) {
                        reviews_html += '<div class="row">';
                    }
                    reviews_html += '<div class="col-sm-6">\
                    <div class="card"> \
                    <div class="card-body">' +
                        '<p class="card-text"><img class="comment-avatar" src="' + reviews[r].avatar + '" height="30">' + reviews[r].author + '</p>' +
                        '<p class="card-text">' + generateStars(reviews[r].score) + '</p>' +
                        '<p class="card-text">Comment: ' + reviews[r].comment + '</p>' +
                        '</div> \
                    </div> \
                    </div>';
                    if (i == 1) {
                        reviews_html += '</div>'
                    }
                    i = (i + 1) % 2;
                }
                if (i == 0) {
                    reviews_html += '</div>'
                }
                $('#review-list').html(reviews_html);
            });
        }
    });
});

function generateStars(score) {
    stars = ['<img class="inline-star" src="/static/assets/img/material-design-icons/svg/ic_star_black_24px.svg">',
        '<img class="inline-star" src="/static/assets/img/material-design-icons/svg/ic_star_half_black_24px.svg">',
        '<img class="inline-star" src="/static/assets/img/material-design-icons/svg/ic_star_border_black_24px.svg">'
    ];
    console.log(stars[0].repeat(Math.floor(score)));
    starhtml = stars[0].repeat(Math.floor(score)) +
        stars[1].repeat(Math.round(score) - Math.floor(score)) +
        stars[2].repeat(5 - Math.ceil(score));
    return starhtml;
}