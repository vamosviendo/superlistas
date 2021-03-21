window.superlistas = {};

window.superlistas.initialize = function() {
  $('input[name="texto"]').on('keypress', function() {
    $(".has-error").hide();
  });
};
