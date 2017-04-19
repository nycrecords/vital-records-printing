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

    var values = [];
    var rotationValues = [];
    var numImages;

    function setNumImages(len) {
        numImages = len;
    }

    function search(empty) {  // empty = true
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
                                var controls = $("#arrow-controls");
                                var indicators = $(".carousel-indicators");
                                var certImages = $(".carousel-inner");
                                setNumImages(response.data.urls.length);
                                certImages.empty();
                                indicators.empty();
                                if (numImages > 1) {
                                    controls.append("<a class='left carousel-control' href='#cert-carousel' role='button' data-slide='prev'>" +
                                        "<span class='glyphicon glyphicon-chevron-left'></span>" +
                                        "</a>"
                                    )
                                    controls.append("<a class='right carousel-control' href='#cert-carousel' role='button' data-slide='next'>" +
                                        "<span class='glyphicon glyphicon-chevron-right'></span>" +
                                        "</a>"
                                    )
                                }
                                for (var i = 0; i < numImages; i++) {
                                    indicators.append("<li data-slide-to='" + i + "' class='" + (i === 0 ? "active" : "") + "'></li>");
                                    certImages.append(
                                        "<div class='item" +
                                        (i === 0 ? " active" : "") +
                                        "'><img class='img-responsive cert-image" +
                                        (i === 0 ? " current" : "") + "' src='" +
                                        response.data.urls[i] + "'></div>"
                                    );
                                }
                                if (numImages == 1) {
                                    $("li.active").css("display", "none");
                                }
                                $("#cert-number").text(response.data.number);
                                $("#cert-type").text(response.data.type);
                                $("#cert-name").text(response.data.name);
                                $("#cert-year").text(response.data.year);
                                $("#cert-county").text(response.data.county);
                                $("#cert-soundex").text(response.data.soundex);
                            },
                            complete: function () {
                                for (var i = 0; i < numImages; i++) {
                                    values[i] = {brightness: 0, contrast: 0};
                                    rotationValues[i] = 0;
                                }
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

    // Only allow digits and '*' in year field
    $("#year").bind({
        keydown: function (e) {
            if (e.shiftKey === true) {
                return e.which === 9 || e.which === 56;
            }
            return !(e.which > 57 || e.which === 32);
        }
    });
    

    // start of camanJS functionality
    var printAll = [];
    var deg = 0;
    var rotate;
    $('input[type=range]').change(applyFilters);

    function applyFilters() {
        var brightness = parseInt($('#brightness').val()),
            cntrst = parseInt($('#contrast').val());
        var current = values[parseInt($("li.active").attr("data-slide-to"))];
        current.brightness = brightness;
        current.contrast = cntrst;

        Caman('.current', function () {
            this.revert(false);
            this.brightness(brightness);
            this.contrast(cntrst);
            this.render();
        });
    }

    $('#reset-btn').on('click', function (e) {
        var current = values[parseInt($("li.active").attr("data-slide-to"))];
        current.brightness = 0;
        current.contrast = 0;

        $('input[type=range]').val(0);
        Caman('.current', function () {
            this.revert(false);
            this.render();
        });

        var index = parseInt($("li.active").attr("data-slide-to"));
        var rotate = 'rotate(' + 360 + 'deg)';
        $('.current').css({
        '-webkit-transform': rotate,
        '-moz-transform': rotate,
        '-o-transform': rotate,
        '-ms-transform': rotate,
        'transform': rotate
        });
        rotationValues[index] = 0;
        deg = 0;
    });

    var printSingleTop = "<html>" +
    "               <head>" +
    "               <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css' integrity='sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u' crossorigin='anonymous'>" +
    "               </head>" +
    "               <body>" +
    "               <table style='text-align: center; width: 8.5in; height: 11in;'" +
    "               <tr>" +
    "               <td>" +
    "               <img ";
    var printSingleBot = "'/>" +
        "               </td>" +
        "               </tr>" +
        "               </table>" +
        "               </body>" +
        "               </html>";

    var printAllTop = "<html><head><link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css' integrity='sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u' crossorigin='anonymous'></head><body>";
    var tableTop = "<table style='text-align: center; width: 8.5in; height: 11in; page-break-before: always;'><tr><td><img ";
    var tableBot = "'/></td></tr></table>";
    var printAllBot = "</body></html>";


    $('#print-btn').on('click', function (e) {
        var rotationStyles = "style='-webkit-transform: rotate(" + rotationValues[0] + "deg); -moz-transform: rotate(" + rotationValues[0] + "deg); -o-transform: rotate(" + rotationValues[0] + "deg); -ms-transform: rotate(" + rotationValues[0] + "deg); transform: rotate(" + rotationValues[0] + "deg);' src='";
        Caman('.current', function () {
            this.render(function () {
                var finalImage = this.toBase64();
                var printWindow = window.open();
                printWindow.document.write(printSingleTop);
                printWindow.document.write(rotationStyles);
                printWindow.document.write(finalImage);
                printWindow.document.write(printSingleBot);
                printWindow.document.close();
                setTimeout(function(){
                    printWindow.print();
                    printWindow.close();
                }, 100);
            });
        });
    });

    $('#print-all-btn').on('click', function (e) {
        $.each($(".cert-image"), function (key, value) {
            Caman(this, function () {
                var image = this.toBase64();
                var rotated = $(value).hasClass('rotate');
                var imageJSON = {image: image, rotated: rotated};
                printAll.push(imageJSON);
            });

        });
        var rotationStyles;
        var convertTimer = setInterval(function () {
            if( printAll.length === $(".cert-image").length) {
                clearInterval(convertTimer);
                var printWindow = window.open();
                printWindow.document.write(printAllTop);
                for (var i = 0; i < printAll.length; i++) {
                    rotationStyles = "style='-webkit-transform: rotate(" + rotationValues[i] + "deg); -moz-transform: rotate(" + rotationValues[i] + "deg); -o-transform: rotate(" + rotationValues[i] + "deg); -ms-transform: rotate(" + rotationValues[i] + "deg); transform: rotate(" + rotationValues[i] + "deg);' src='";
                    printWindow.document.write(tableTop);
                    printWindow.document.write(rotationStyles);
                    printWindow.document.write(printAll[i].image);
                    printWindow.document.write(tableBot);
                }
                printWindow.document.write(printAllBot);
                printWindow.document.close();
                setTimeout(function(){
                    printWindow.print();
                    printWindow.close();
                }, 100);
            }
        }, 1000);
        printAll = [];
    });


    function addPadding(){
        var modalHeight = $('.carousel-inner').height();
        var imageHeight = $('.current').height();
        var rotationPadding = Math.ceil((imageHeight - modalHeight) / 2);
        $('.carousel-inner').css({'padding-top': rotationPadding + 'px', 'padding-bottom': rotationPadding + 'px'});
    }

    $('#toggle-image-view-btn').click(function () {
        $('.current').toggleClass('fit-to-screen');
        var modalHeight = $(window).height() + 'px';
        if ($('.current').hasClass('fit-to-screen')){
            // $('#carousel-body').css('height', modalHeight);
            $('.current').css({'max-height': '35%', 'max-width': '35%'});
            $('#toggle-image-view-btn').text('View Full Image ');
            $('#toggle-image-view-btn').append('<span class="glyphicon glyphicon-resize-full"></span>');
        }
        else{
            $('.current').css({'max-height': '100%', 'max-width': '100%'});
            $('#toggle-image-view-btn').text('Fit To Screen ');
            $('#toggle-image-view-btn').append('<span class="glyphicon glyphicon-resize-small"></span>');
        }
        addPadding();
    });

    // reset brightness & contrast on hide modal
    $('#cert-modal').on('hidden.bs.modal', function () {
        $.each($(".item"), function (key, value) {
            $(".current").removeClass("current");
            $(value).find(".cert-image").addClass("current");
            Caman('.current', function () {
                this.revert(false);
                this.render();
            });
        });
        $('input[type=range]').val(0);
        $(".carousel-indicators").empty();
        $(".carousel-inner").empty();
        $(".carousel-inner").append("<img src='/static/img/spinner.gif' style='width:200px;height:200px;'>");
        deg = 0;
        rotate = '';
    });

    $('#cert-carousel').bind('slid.bs.carousel', function (e) {
        var current = values[parseInt($("li.active").attr("data-slide-to"))];
        $("#brightness").val(current.brightness);
        $("#contrast").val(current.contrast);
        $(".current").removeClass("current");
        $(".item.active").find(".cert-image").addClass("current");
        var index = parseInt($("li.active").attr("data-slide-to"));
        deg = rotationValues[index];
        rotate = '';
        // set the toggle button text and functionality
        if ($('.current').hasClass('fit-to-screen')) {
            $('#toggle-image-view-btn').text('View Full Image ');
            $('#toggle-image-view-btn').append('<span class="glyphicon glyphicon-resize-full"></span>');
        }
        else {
            $('#toggle-image-view-btn').text('Fit To Screen ');
            $('#toggle-image-view-btn').append('<span class="glyphicon glyphicon-resize-small"></span>');
        }
        addPadding();
    });

    $('#rotate-right-btn').click(function () {
        deg = deg + 90;
        if (deg === 360) deg = 0;
        rotate = 'rotate(' + deg + 'deg)'
        $('.current').css({
        '-webkit-transform': rotate,
        '-moz-transform': rotate,
        '-o-transform': rotate,
        '-ms-transform': rotate,
        'transform': rotate
        });
        var index = parseInt($("li.active").attr("data-slide-to"));
        rotationValues[index] = deg;
        
        // add padding to top and bottom of rotated image
        addPadding();
    });

    $('#rotate-left-btn').click(function () {
        deg = deg - 90;
        if (deg === -360) deg = 0;
        rotate = 'rotate(' + deg + 'deg)'
        $('.current').css({
        '-webkit-transform': rotate,
        '-moz-transform': rotate,
        '-o-transform': rotate,
        '-ms-transform': rotate,
        'transform': rotate
        });
        var index = parseInt($("li.active").attr("data-slide-to"));
        rotationValues[index] = deg;
        
        // add padding to top and bottom of rotated image
        addPadding();
    });
    // end of camanJS functionality
});