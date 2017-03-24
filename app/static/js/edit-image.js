$(function () {
    $('input[type=range]').change(applyFilters);

    function applyFilters() {
        var brightness = parseInt($('#brightness').val());
        var cntrst = parseInt($('#contrast').val());

        Caman('#cert-image', function () {
            this.revert(false);
            this.brightness(brightness);
            this.contrast(cntrst);
            this.render();
        });
    }

    $('#resetbtn').on('click', function (e) {
        $('input[type=range]').val(0);
        Caman('#cert-image', function () {
            this.revert(false);
            this.render();
        });
    });

    $('#printbtn').on('click', function (e) {
        Caman('#cert-image', function () {
            this.render(function () {
                var finalImage = this.toBase64();
                var printWindow = window.open();
                printWindow.document.write('<html><body><img width=2000 src="');
                printWindow.document.write(finalImage);
                printWindow.document.write('" /></body></html>');
                printWindow.document.close();
                printWindow.print();
                printWindow.close();
            });
        });
    });

    $('#toggle-image-view-btn').click(function () {
        $('#modal-image').toggleClass("image-modal-body");
    });

    $('#myModal').on('hidden.bs.modal', function () {
        $('input[type=range]').val(0);
        Caman('#cert-image', function () {
            this.revert(false);
            this.render();
        });
    });
});