Caman("#image-id", function () {
  
});

$('input[type=range]').change(applyFilters);

function applyFilters() {
  var brightness = parseInt($('#brightness').val());
  var cntrst = parseInt($('#contrast').val());

    Caman('#image-id', function() {
      this.revert(false);
      this.brightness(brightness);
      this.contrast(cntrst);
      this.render();
    });
}



$('#increase-brightness-btn').on('click', function(e) {
  var current = document.getElementById("increase-brightness-btn").value;
  Caman('#image-id', function() {
    this.brightness(current + 5);
    this.render();
    current = current + 5;
  });

});

$('#decrease-brightness-btn').on('click', function(e) {
  var current = document.getElementById("increase-brightness-btn").value;
  Caman('#image-id', function() {
    this.brightness(current - 5);
    this.render();
    current = current - 5;
  });
});


$('#increase-contrast-btn').on('click', function(e) {
  Caman('#image-id', function() {
    this.contrast(5);
    this.render();
  });
});

$('#decrease-contrast-btn').on('click', function(e) {
  Caman('#image-id', function() {
    this.contrast(-5);
    this.render();
  });
});


$('#resetbtn').on('click', function(e) {
  $('input[type=range]').val(0);
  Caman('#image-id', function() {
    this.revert(false);
    this.render();
  });
});


$('#savebtn').on('click', function(e) {
  Caman('#image-id', function() {
    this.render(function() {
      this.save('png');
    });
  });
});

