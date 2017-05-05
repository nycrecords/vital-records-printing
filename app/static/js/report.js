$(document).ready(function(){
    var firstIndicator = $('.indicator').first(), 
        imageItems = $('.item'),
        controls = $("#arrow-controls");
    firstIndicator.first().addClass("active");
    imageItems.first().addClass("active");
    if (imageItems.length > 1) {
        controls.append("<a class='left carousel-control' href='#cert-carousel' role='button' data-slide='prev'>" +
            "<span class='glyphicon glyphicon-chevron-left'></span>" +
            "</a>"
        );
        controls.append("<a class='right carousel-control' href='#cert-carousel' role='button' data-slide='next'>" +
            "<span class='glyphicon glyphicon-chevron-right'></span>" +
            "</a>"
        );
    }
});
