(function ($) {
    function tipoCode(tipo) {
        if (/individual/i.test(tipo)){
            return('INDV')
        } else if (/institucional/i.test(tipo)) {
            return('INST')
        }
        else if(/corporativo/i.test(tipo)) {
            return('CORP')
        } else {
            return('Seleccione Tipo de donante')
        }
        
    }
  $(document).ready(function () {
    console.log("is created!!");
    $(".field-nombre input, .field-tipo select").change(function () {
        let tipo = $('.field-tipo select option:selected').text();
        tipo = tipoCode(tipo)
        let nombre =  $('.field-nombre input').val().replace(/ /g, '_').substring(0, 20).toUpperCase() 
        $('.field-codigo input').val(tipo+'-'+nombre);
    });

    //Disables editable field, input data generated by code
    $(".field-codigo input").prop("disabled", true);
    //Enabled disabled before save, to allow saving of object
    $(".submit-row input").click(function () {
      $(".field-codigo input").prop("disabled", false);
    });
  });
})(django.jQuery);
