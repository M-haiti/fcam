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

    $(".field-propuesta_vinculada select").change(function () {
      console.log("Generar Codigo 3");
      let count = 0;
      let url = "/countinformefinal/";
      let paiscode = "";
      let duracionProp = "";
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
          duracion = $("#ajax_result .duracionprop").text();
          console.log("duracion", duracion);
          console.log("count", count);
          let codigo_org = $(
            ".field-propuesta_vinculada select option:selected"
          ).text();
          suffix = "";
          if (duracion == "None") {
            codigo_org = "";
           
            alert(
              "La propuesta seleccionada no tiene definida su duración. No se puede crear un informe hasta que la propuesta tenga su duración definida."
            );
          } else if (count == 0 && duracion == "12M") {
            if (count == 0) {
              suffix = "-I.Final(12M)";
              codigo_org = codigo_org + suffix;
            } else if (count >= 1) {
              codigo_org = "";
              alert(
                "La propuesta de 12 meses ya tiene un informe final existente. No puede tener más. Busque un informe final existente o cambie la duración de la propuesta."
              );
            }
          } else if (duracion == "18M") {
            if (count == 0) {
              suffix = "-I.Final(18M)";
              codigo_org = codigo_org + suffix;
            } else if (count == 1) {
              codigo_org = "";
              alert(
                "La propuesta de 18 meses ya tiene un informe final existente. Busque un informe final existente o cambie la duración de la propuesta."
              );
            }
          } else if (duracion == "24M") {
            if (count == 0) {
              suffix = "-I.SemiFinal(12M)";
              codigo_org = codigo_org + suffix;
            } else if (count == 1) {
              suffix = "-I.Final(24M)";
              codigo_org = codigo_org + suffix;
            } else if (count >= 2) {
              suffix = "";
              alert(
                "La propuesta de 24 meses ya tiene dos informes finales existentes. Busque un informe final existente o cambie la duración de la propuesta."
              );
            }
          } else if (duracion == "36M") {
            if (count == 0) {
              suffix = "-I.SemiFinal(12M)";
              codigo_org = codigo_org + suffix;
            } else if (count == 1) {
              suffix = "-I.SemiFinal(24M)";
              codigo_org = codigo_org + suffix;
            } else if (count == 2) {
              suffix = "-I.Final(36M)";
              codigo_org = codigo_org + suffix;
            } else if (count >= 3) {
              suffix = "";
              alert(
                "La propuesta de 36 meses ya tiene tres informes finales existentes. No puede tener más. Agregue un informe final o cambie la duración de la propuesta."
              );
            }
          }
          console.log("codigo_org", codigo_org);
          $(".field-codigo_prop input").val(codigo_org);
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
    console.log("Generar Codigo 11");
    generarCodigo();
    moveInlines(
      "#programa-contacto-content_type-object_id-group",
      "#content-main>form>div>fieldset:nth-child(2)"
    );
    moveInlines(
      "#programa-grupoactor-content_type-object_id-group",
      "#content-main>form>div>fieldset:nth-child(2)"
    );
    //Triggers rename in case of validation error whilst trying to save
    if ($(".errornote").length) {
      $(".field-propuesta_vinculada select").trigger("change");
    }

    //Disabled components
    $(".field-codigo_prop input").prop("disabled", true);
    $("[id^=id_programa-comment]").prop("disabled", true);
    //Enabled disabled before save, to allow saving of object
    $(".submit-row input").click(function () {
      console.log("remove disabled!");
      $(".field-codigo_prop input").prop("disabled", false);
      $("[id^=id_programa-comment]").prop("disabled", false);
    });
  });
})(django.jQuery);
