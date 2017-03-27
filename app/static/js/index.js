$(function () {
    var popover = $('[data-toggle="popover"]');
    popover.popover({
        html: true
    });

    $('body').on('click', function (e) {
        // hide popover if click occurs outside of it
        if ($(e.target).data('toggle') !== 'popover' &&
            $(e.target).parents('.popover.in').length === 0) {
            popover.popover('hide');
        }
    }).on('hidden.bs.popover', function (e) {
        // ensure only 1 click is required to show popover after hiding
        $(e.target).data("bs.popover").inState.click = false;
    });
});