// Caman("#test", "./static/img/test_pic.jpg", function () {
//   // manipulate image here
//   this.brightness(40).render();
// });


function myFunction() {
    document.getElementsByTagName("H1")[0].setAttribute("class", "democlass"); 
}

var vintage = $('#vintagebtn');

Caman("#canvas-id", "./static/img/test_pic.jpg", function () {
    // manipulate image here
    // this.brightness(0).render();
    // this.contrast(0).render();
    // // this.sinCity().render();
    // // this.vintage().render();
});

// vintage.on('click', function(e) {
//   Caman('#canvas-id', function() {
//     this.vintage().render();
//   });
// });

vintage.on('click', function(e) {
  Caman('#canvas-id', "./static/img/test_pic.jpg", function() {
    this.vintage().render();
      this.brightness(50).render();
    this.contrast(0).render();
  });
});


$('input[type=range]').change(applyFilters);

function applyFilters() {
  var brightness = parseInt($('#brightness').val());
  var cntrst = parseInt($('#contrast').val());

    Caman('#canvas-id', './static/img/test_pic.jpg', function() {
      this.revert(false);
      this.brightness(brightness);
      this.contrast(cntrst);
      this.render();
    });
}