$('input[type=range]').change(applyFilters);

function applyFilters() {
  var brightness = parseInt($('#brightness').val());
  var cntrst = parseInt($('#contrast').val());

    Caman('#cert-image', function() {
      this.revert(false);
      this.brightness(brightness);
      this.contrast(cntrst);
      this.render();
    });
}

$('#resetbtn').on('click', function(e) {
  $('input[type=range]').val(0);
  Caman('#cert-image', function() {
    this.revert(false);
    this.render();
  });
});