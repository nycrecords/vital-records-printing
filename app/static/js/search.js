$(function () {
    var spinner = $("#spinner");
    spinner.hide();

    var searchForm = $("#search-form");

    searchForm.submit(function (e) {
        e.preventDefault();
        search();
    });

    window.onscroll = function () {
        if ((window.innerHeight + window.scrollY) >= document.body.scrollHeight) {
            // you're at the bottom of the page
            var prevValue = parseInt($('#start').val());
            var limit = 20;
            $('#start').val(prevValue + limit);
            search(false);
        }
    };

    function search(empty) {
        if (typeof empty === 'undefined') {
            empty = true;
        }
        if (!empty) {
            spinner.show();
        }
        $.ajax({
            url: "/search",
            method: "post",
            data: searchForm.serialize(),
            success: function (response) {
                $(".type").text('');
                $(".county").text('');
                $(".year").text('');
                $(".soundex").text('');

                if (response.hasOwnProperty('errors')) {
                    console.log(response.errors);
                    $(".type").text(response.errors.type);
                    $(".county").text(response.errors.county);
                    $(".year").text(response.errors.year);
                    $(".soundex").text(response.errors.soundex);
                }
                else {
                    var results = $("#results");
                    empty && results.empty();
                    for (var i = 0; i < response.data.length; i++) {
                        results.append(response.data[i]);
                    }
                }
                if (!empty) {
                    spinner.hide();
                }
            }
        });
    }


    // Sorting
    var sortOrderToGlyphicon = {
        desc: "glyphicon-triangle-bottom",
        asc: "glyphicon-triangle-top",
        none: ""
    };

    var sortSequence = ["none", "desc", "asc"];

    function cycleSort(elem) {
        var icon = elem.find(".glyphicon");
        icon.removeClass(sortOrderToGlyphicon[elem.attr("data-sort-order")]);

        elem.attr(
            "data-sort-order",
            sortSequence[
            (sortSequence.indexOf(elem.attr("data-sort-order")) + 1 + sortSequence.length)
            % sortSequence.length]);

        icon.addClass(sortOrderToGlyphicon[elem.attr("data-sort-order")]);
    }

    $(".sort-field").click(function () {
        cycleSort($(this));
        // fill hidden inputs
        $("#" + $(this).attr("data-target")).val($(this).attr("data-sort-order"));
        // clear sorting from other columns
        $.each($(".sort-field").not($(this)), function (key, value) {
            var elem = $(value);
            $("#" + elem.attr("data-target")).val("none");
            var icon = elem.find(".glyphicon");
            icon.removeClass(sortOrderToGlyphicon[elem.attr("data-sort-order")]);
            elem.attr("data-sort-order", "none");
        });
        $("#search-form").submit();
    });
});

