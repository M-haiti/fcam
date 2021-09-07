(function ($) {
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = $.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) == name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    //RETORNANDO EL TOKEN
    return cookieValue;
  } //end function getCookie
  function generarCodigo() {
    console.log("Generar Codigo 2");

    $(".field-prop_ic_vincula select").change(function () {
      console.log("Generar Codigo 3");
      let count = 0;
      let url = "/countinfic/";
      let prop_ic_id = "";
      prop_ic_id = $(this).val();
      prop_ic_code = $('.field-prop_ic_vincula select option:selected').text();
      url += prop_ic_id;

      console.log("url", url);

      let csrftoken = getCookie("csrftoken");

      $.ajax({
        type: "POST",
        url: url,
        data: {
          csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
          $("<div id='ajax_result'></div>").appendTo(document.body);
          $(data).appendTo($("#ajax_result"));
          count = parseInt($("#ajax_result .conteo").text());
          console.log("count", count);
          count++
          codigo_inf_ic = prop_ic_code +'-'+count
          console.log("codigo_inf_ic",  codigo_inf_ic);
          $(".field-codigo_inf_ic input").val(codigo_inf_ic);
          $("#ajax_result").remove();
        },
        error: function (jqXHR, textStatus, errorThrown) {
          if (jqXHR.status === 0) {
            alert(
              "Error al intentar Conectarse: Verifique su conexion a Internet."
            );
          } else if (jqXHR.status == 404) {
            alert("La Pagina solicitada no fue encontrada [404]");
          } else if (jqXHR.status == 500) {
            alert("Erro Interno [500]");
          } else if (textStatus === "parsererror") {
            alert("Error en el retorno de Datos. [parseJson]");
          } else if (textStatus === "timeout") {
            alert("Tiempo de Espera agotado");
          } else if (textStatus === "abort") {
            alert("Solicitud Abortada. [Ajax Request]");
          } else {
            alert("Error desconocido: " + jqXHR.responseText);
          }
          "#ajax_result".remove(); //end if
        }, //end error
      });
    });
  }
  function moveInlines(sel, moveTo) {
    $(sel).detach().appendTo(moveTo);
  }
  $(document).ready(function () {
    console.log("Generar Codigo 1");
    generarCodigo();

    //Triggers rename in case of validation error whilst trying to save
    if ($(".errornote").length) {
      $(".field-propuesta_vinculada select").trigger("change");
    }

    //Disabled components
    $(".field-codigo_inf_ic input").prop("disabled", true);
    //Enabled disabled before save, to allow saving of object
    $(".submit-row input").click(function () {
      console.log("remove disabled!");
      $(".field-codigo_inf_ic input").prop("disabled", false);
    });
  });
})(django.jQuery);
