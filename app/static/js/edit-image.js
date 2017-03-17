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


$('#savebtn').on('click', function(e) {
  Caman('#cert-image', function() {
    this.render(function() {
      this.save('jpg');
    });
  });
});


function toggleMode(){
  if(document.getElementById("interactive-mode").checked){
    document.getElementById("brightness").setAttribute("oninput", "applyFilters()");
    document.getElementById("contrast").setAttribute("oninput", "applyFilters()");
  }
  else{
    document.getElementById("brightness").setAttribute("oninput", "");
    document.getElementById("contrast").setAttribute("oninput", "");
  }
}