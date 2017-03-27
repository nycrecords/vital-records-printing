$(function () {
    var spinner = $("#spinner");
    spinner.hide();

    var searchForm = $("#search-form");

    searchForm.submit(function (e) {
        e.preventDefault();
        search();
    });

    var loadMoreBtn = $("#load-more");
    loadMoreBtn.hide();
    loadMoreBtn.click(function () {
        if ($("#results").children().length > 0) {
            var start = $("#start");
            var prevValue = parseInt(start.val());
            var limit = 20;
            $(start).val(prevValue + limit);
            search(false);
        }
    });

    function search(empty) {
        loadMoreBtn.hide();
        if (typeof empty === 'undefined') {
            empty = true;
        }
        if (!empty) {
            spinner.show();
        }
        else {
            $('#start').val(0);
        }
        $.ajax({
            url: "/search",
            method: "post",
            data: searchForm.serialize(),
            success: function (response) {
                $(".type").text('');  // TODO: make it obvious that this pertains to errors
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
                    // show load more button
                    if (response.data.length > 0) {
                        loadMoreBtn.show();
                    }
                    // empty results if needed, and add new set
                    var results = $("#results");
                    empty && results.empty();
                    for (var i = 0; i < response.data.length; i++) {
                        results.append(response.data[i]);
                    }
                    // bind click event for modal to result rows
                    $(".result-row").click(function (e) {
                        e.preventDefault();
                        $.ajax({
                            url: "/certificate/" + $(this).attr("id"),
                            success: function (response) {
                                $("#cert-image").attr("src", response.data.src);
                                $("#cert-number").text(response.data.number);
                                $("#cert-type").text(response.data.type);
                                $("#cert-name").text(response.data.name);
                                $("#cert-year").text(response.data.year);
                                $("#cert-county").text(response.data.county);
                                $("#cert-soundex").text(response.data.soundex);
                            }
                        });
                    });
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