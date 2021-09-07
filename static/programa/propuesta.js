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

    $(".field-codigo_org select").change(function () {
      console.log("Generar Codigo 3");
      let count = 0
      let url = "/countpropuesta/";
      let paiscode = "";
      paiscode = $(this).val();
      url += paiscode;

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
          let codigo_org = $(".field-codigo_org select option:selected").text();
          console.log("codigo_org: ", codigo_org);
          console.log("count1: ", count);
          if (count==0) {
            console.log("count2: ", count);
          } else {
            count = $("#ajax_result td").first().text();
            console.log("count3.1: ", count);
            count = count.substr(count.lastIndexOf("-") + 1, 4);
            count = parseInt(count);
            console.log("count3.2: ", count);
          }
          count++;
          console.log("count4: ", count);

          codigo_org = codigo_org + "-" + count;
          $(".field-codigo_prop input").val(codigo_org);
          $('#ajax_result').remove();
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
          $('#ajax_result').remove(); //end if
        }, //end error
      });
    });
  }
  function moveInlines(sel, moveTo){
      $(sel).detach().appendTo(moveTo);
  }
  $(document).ready(function () {
    console.log("Generar Codigo 1");
    generarCodigo();
    moveInlines('#programa-contacto-content_type-object_id-group','#content-main>form>div>fieldset:nth-child(2)')
    moveInlines('#programa-grupoactor-content_type-object_id-group','#content-main>form>div>fieldset:nth-child(2)')
    //Triggers rename in case of validation error whilst trying to save
    if ($(".errornote").length) {
        $(".field-codigo_org select").trigger("change");
    }
    
    //Disabled components
    $(".field-codigo_prop").prop("disabled", true);
    $("[id^=id_programa-comment]").prop("disabled", true);
    //Enabled disabled before save, to allow saving of object
    $(".submit-row input").click(function () {
      console.log("remove disabled!");
      $(".field-codigo_prop input").prop("disabled", false);
      $("[id^=id_programa-comment]").prop("disabled", false);
    });
  });
})(django.jQuery);
