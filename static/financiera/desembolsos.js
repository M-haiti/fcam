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
    $(".field-fecha_desembolso #id_fecha_desembolso_year").change(function () {
      console.log("Generar Codigo 4");

      let ano = $(
        ".field-fecha_desembolso #id_fecha_desembolso_year option:selected"
      ).text();
      console.log("ano", ano);
      let count = "";
      let url = "/countdesembolsos/" + ano;

      console.log("url", url);

      let csrftoken = getCookie("csrftoken");

      $.ajax({
        type: "POST",
        url: url,
        data: {
          csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
          count = parseInt(data);
          isNaN(count) ? (count = 0) : count;
          count++;
          codigoOrg = "Desembolso-" + ano + "-" + count;
          $(".field-codigo input").val(codigoOrg);
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
          } //end if
        }, //end error
      });
    });
  }
  function removealltables() {
    console.log("Removealltables!")
    $("#ajax_result.desembolsosae").remove();
    $("#ajax_result.desembolsosprop").remove();
  }
  function displayDesembolsosProp() {
    $(".field-propuesta select").change(function () {
      console.log("Generar displayDesembolsosProp");


      let propuesta = $("option:selected", this).val();
      console.log("ano", propuesta);
      let url = "/displaydesembolsosprop/" + propuesta;

      console.log("url", url);

      let csrftoken = getCookie("csrftoken");

      $.ajax({
        type: "POST",
        url: url,
        data: {
          csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
          $("#ajax_result.desembolsosprop").remove();
          $("<div id='ajax_result' class='desembolsosprop'></div>").insertAfter(
            ".field-propuesta select"
          );
          $(data).appendTo($("#ajax_result"));
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
          } //end if
        }, //end error
      });
    });
  }
  function displayDesembolsosAe() {
    $(".field-apoyo_estrategico select").change(function () {
      console.log("Generar displayDesembolsosAe");

      

      let propuesta = $("option:selected", this).val();
      console.log("ano", propuesta);
      let url = "/displaydesembolsosae/" + propuesta;
                  
      console.log("url", url);

      let csrftoken = getCookie("csrftoken");

      $.ajax({
        type: "POST",
        url: url,
        data: {
          csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
          console.log("Success!");
          $("#ajax_result.desembolsosae").remove();
          $("<div id='ajax_result' class='desembolsosae'></div>").insertAfter(
            ".field-apoyo_estrategico select"
          );
          $(data).appendTo($("#ajax_result.desembolsosae"));
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
          } //end if
        }, //end error
      });
    });
  }

  function displayDesembolsosIc() {
    $(".field-iniciativa_conjunta select").change(function () {
      console.log("Generar displayDesembolsosIC");

      

      let propuesta = $("option:selected", this).val();
      console.log("ano", propuesta);
      let url = "/displaydesembolsosic/" + propuesta;
                  
      console.log("url", url);

      let csrftoken = getCookie("csrftoken");

      $.ajax({
        type: "POST",
        url: url,
        data: {
          csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
          console.log("Success!");
          $("#ajax_result.desembolsosic").remove();
          $("<div id='ajax_result' class='desembolsosic'></div>").insertAfter(
            ".field-iniciativa_conjunta select"
          );
          $(data).appendTo($("#ajax_result.desembolsosic"));
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
          } //end if
        }, //end error
      });
    });
  }

  function displayIngreso() {
    $(".field-ingreso_vinculado select").change(function () {
      console.log("Generar displayIngreso()");

      let ingreso = $("option:selected", this).val();
      console.log("ingreso", ingreso);
      let url = "/displayingreso/" + ingreso;

      console.log("url", url);

      let csrftoken = getCookie("csrftoken");

      $.ajax({
        type: "POST",
        url: url,
        data: {
          csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
          $("#ajax_result.ingreso").remove();
          $("<div id='ajax_result' class='ingreso'></div>").insertAfter(
            ".field-ingreso_vinculado select"
          );
          $(data).appendTo($("#ajax_result.ingreso"));
          $(".balancetiemporeal").remove();
          orderRows(".field-ingreso_vinculado .distporprograma")
          orderRows(".field-ingreso_vinculado .distporic")
          orderRows(".field-ingreso_vinculado .distporae")
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
          } //end if
        }, //end error
      });
    });
  }
  function showHideItems(firstrun) {
    //Delete previous tables
    //removealltables()
    
    //Slide everything up
    $(".field-propuesta").slideUp();
    $(".field-apoyo_estrategico").slideUp();
    $(".field-iniciativa_conjunta").slideUp();

    //Cleans selection, a shows fields needed
    $(".field-tipo_org select").change(function () {
      if (firstrun===false) {
        //Select nothing o all selectors
        $(".field-propuesta select, .field-apoyo_estrategico select, .field-iniciativa_conjunta select").val("");
      }
      firstrun = false
      switch ($("option:selected", this).text()) {
        case "Iniciativa conjunta":
          displayDesembolsosIc();
          $(".field-propuesta").slideUp();
          $(".field-apoyo_estrategico").slideUp();
          $(".field-iniciativa_conjunta").slideDown();
          console.log("Iniciativa conjunta");
          break;
        case "Coparte": 
          displayDesembolsosProp();
          $(".field-propuesta select").trigger("change");  
          $(".field-propuesta").slideDown();
          $(".field-apoyo_estrategico").slideUp();
          $(".field-iniciativa_conjunta").slideUp();
          console.log("Coparte");
          break;
        case "Apoyo estratégico":
          displayDesembolsosAe();
          $(".field-apoyo_estrategico select").trigger("change");
          $(".field-propuesta").slideUp();
          $(".field-apoyo_estrategico").slideDown();
          $(".field-iniciativa_conjunta").slideUp();
          console.log("Apoyo Estratégico");
      }
    });
  }
  function orderRows(sel) {
    let paste=sel;
    sel = sel + " tbody tr"
    console.log('sel', sel)
    //$(".balancetiemporeal").remove();
    console.log("Order Rows!");
    let optionsList = [""];
    //let counteradded = 1
    let flagfirstvalue = true;
    let flagNewValue = false;

    //Checks programa value line by line, and generates list of unique values
    //$(".field-ingreso_vinculado .distporprograma tbody tr").each(function () {
    $(sel).each(function () {  
      let val = String($("td:nth-child(3)", this).text());
      //Builds list from non repeating values
      for (i = 0; i < optionsList.length; i++) {
        if (optionsList[i] === val) {
          flagNewValue = false;
          break;
        } else {
          flagNewValue = true;
        }
      }
      if (flagNewValue === true) {
        if (flagfirstvalue) {
          optionsList[0] = val;
          flagfirstvalue = false;
        } else {
          optionsList.push(val);
        }
      }
      console.log("optionList", optionsList);
      flagNewValue = false;
    });

    //Sums Ingreos and Desembolsos calculates balance for each program
    let balanceOK = true;
    for (i = 0; i < optionsList.length; i++) {
      let ingresos = 0;
      let desembolsos = 0;
      balance = 0;
      //$(".field-ingreso_vinculado .distporprograma tbody tr").each(function () {
      $(sel).each(function () {  
        let val = String($("td:nth-child(3)", this).text());
        if (optionsList[i] === val) {
          if ($("td:nth-child(1)", this).text() === "+") {
            ingresos += parseInt($("td:nth-child(4)", this).text());
          } else {
            desembolsos += parseInt($("td:nth-child(4)", this).text());
          }
        }
      });
      balance = ingresos - desembolsos;
      if (balance < 0) {
        balanceOK = false;
        //console.log("balanceOK False", balance);
      }
      //console.log("optionsList[i]", optionsList[i]);
      //console.log("ingresos", ingresos);
      console.log('paste', paste)
      $(paste).after(
        "<table class='balancetiemporeal' style='float:left;margin:0 2% 5% 0;'><caption  style='background-color:#96c93d'>" +
          optionsList[i] +
          "</caption><tr><td>Ingresos:</td><td>" +
          ingresos +
          "</td></tr><tr><td>Desembolsos:</td><td>" +
          desembolsos +
          "</td></tr><tr><td>Balance:</td><td>" +
          balance +
          "</td></tr></table>"
      );
      //console.log("balance", balance);
    }
    //console.log("balanceOk", balanceOK);
    $(".alert-balance").remove();
    if (balanceOK === false) {
      $(".submit-row input").prop("disabled", true);
      $(".submit-row")
        .last()
        .prepend(
          "<div class='alert alert-danger alert-balance' role='alert'>Balance negativo, corrija el monto para guardar</div>"
        );
    } else {
      $(".submit-row input").prop("disabled", false);
    }
    sel =''
  }
  function calculoBalance() {
    $(".field-monto_total_USD input").change(function () {
      updateMonto = parseInt($(this).val());
      codigo = $(".field-codigo input").val();
      console.log("codigo", codigo);
      $("td:contains(" + codigo + ")")
        .next()
        .next()
        .text(updateMonto);
      orderRows(".field-ingreso_vinculado .distporprograma")
      orderRows(".field-ingreso_vinculado .distporic")
      orderRows(".field-ingreso_vinculado .distporae")
    });
  }
  $(document).ready(function () {
    generarCodigo();
    showHideItems(true);
    displayIngreso();
    calculoBalance();
    $(
      ".field-tipo_org select, select#id_ingreso_vinculado"
    ).trigger("change");
  });
})(django.jQuery);
