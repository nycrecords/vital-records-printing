$(function () {
    var RESULT_SET_LIMIT = 20;

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
            $(start).val(prevValue + RESULT_SET_LIMIT);
            search(false);
        }
    });

    // set year range on input change
    var inputType = $("#type"),
        inputCounty = $("#county"),
        yearRange = $("#year-range");

    [inputType, inputCounty].map(function (input) {
        input.change(setYearRange);
    });

    function setYearRange() {
        $.ajax({
            url: "/years",
            data: {
                "type": inputType.val(),
                "county": inputCounty.val()
            },
            success: function (response) {
                if (response.data !== undefined) {
                    yearRange.text(response.data.start + " - " + response.data.end);
                }
                else {
                    yearRange.text('');
                }
            }
        });
    }

    // set year range on page load
    setYearRange();

    /* TODO: fill me in! */
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
                var errType = $("#error-type"),
                    errCounty = $("#error-county"),
                    errYear = $("#error-year"),
                    errSoundex = $("#error-soundex");

                // clear errors
                [errType, errCounty, errYear, errSoundex]
                    .map(function (err) {
                        err.text('');
                        err.parents(".form-group").removeClass("has-error");
                    });

                if (response.hasOwnProperty('errors')) {
                    // display errors
                    [
                        [errType, response.errors.type],
                        [errCounty, response.errors.county],
                        [errYear, response.errors.year],
                        [errSoundex, response.errors.soundex]
                    ].map(function (errDataPair) {
                        if (errDataPair[1]) {
                            errDataPair[0].parents(".form-group").addClass("has-error");
                            errDataPair[0].text(errDataPair[1][0]);  // only show first error in list
                        }
                    });
                }
                else {
                    // show load more button
                    if (response.data.length === RESULT_SET_LIMIT) {
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