$(function () {
    var values = [];
    values[0] = {brightness: 0, contrast: 0};
    values[1] = {brightness: 0, contrast: 0};
    values[2] = {brightness: 0, contrast: 0};
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

    $('#resetbtn').on('click', function (e) {
        var current = values[parseInt($("li.active").attr("data-slide-to"))];
        current.brightness = 0;
        current.contrast = 0;

        $('input[type=range]').val(0);
        Caman('.current', function () {
            this.revert(false);
            this.render();
        });
    });


    var printHTMLtop = "<html>" +
        "               <body>" +
        "               <table style='text-align: center; width: 8.5in; height: 11in;'" +
        "               <tr>" +
        "               <td>" +
        "               <img src='";
    var printHTMLbot = "'/>" +
        "               </td>" +
        "               </tr>" +
        "               </table>" +
        "               </body>" +
        "               </html>";

    $('#printbtn').on('click', function (e) {
        Caman('.current', function () {
            this.render(function () {
                var finalImage = this.toBase64();
                var printWindow = window.open();
                printWindow.document.write(printHTMLtop);
                printWindow.document.write(finalImage);
                printWindow.document.write(printHTMLbot);
                printWindow.document.close();
                printWindow.print();
                // printWindow.close();
            });
        });
    });

    // $('#printbtn').on('click', function (e) {
    //     Caman('.current', function () {
    //         this.render(function () {
    //             var finalImage = this.toBase64();
    //             var printWindow = window.open();
    //             printWindow.document.write('<html><body><img class="test" src="');
    //             printWindow.document.write(finalImage);
    //             printWindow.document.write('" /> <img class="test" src="');
    //             printWindow.document.write(finalImage);
    //             printWindow.document.write('"/></body></html>');
    //             printWindow.document.close();
    //             printWindow.print();
    //             printWindow.close();
    //         });
    //     });
    // });

    $('#print-all-btn').on('click', function (e) {
        Caman('.current', function () {
            this.render(function () {
                var finalImage = this.toBase64();
                var printWindow = window.open();
                printWindow.document.write('<html><body><img class="test" src="');
                printWindow.document.write(finalImage);
                printWindow.document.write('" /> <img class="test" src="');
                printWindow.document.write(finalImage);
                               printWindow.document.write('" /> <img class="test" src="');
                printWindow.document.write(finalImage);
                               printWindow.document.write('" /> <img class="test" src="');
                printWindow.document.write(finalImage);
                printWindow.document.write('"/></body></html>');
                printWindow.document.close();
                printWindow.print();
                printWindow.close();
            });
        });
    });

    $('#toggle-image-view-btn').click(function () {
        $('.modal-body').toggleClass("image-modal-body");
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
    });

    $('#carousel-example-generic').bind('slid.bs.carousel', function (e) {
        var current = values[parseInt($("li.active").attr("data-slide-to"))];
        $("#brightness").val(current.brightness);
        $("#contrast").val(current.contrast);
        $(".current").removeClass("current");
        $(".item.active").find(".cert-image").addClass("current");
    });
});


