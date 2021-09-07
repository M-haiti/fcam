(function ($) {
    function moveInlines(sel, moveTo){
        $(sel).detach().appendTo(moveTo);
    }
    //Disables editing on comment bodies that have content
    function disabledCommentBodyEditing() {
      console.log('Disabling edit on comment bodies with content')  
      $('#programa-comment-content_type-object_id-group textarea').each(function () {
        if ($(this).text()!==""){
          $(this).prop( 'disabled', true );
          $(this).parent().parent().parent().slideUp();
        }
      })
    }
    $(document).ready(function () {
      console.log("Informeintermedio edit!");
      disabledCommentBodyEditing()

      $('#programa-comment-content_type-object_id-group select').prop( 'disabled', true );
      $('.submit-row input').click(function(){
        $('#programa-comment-content_type-object_id-group select').prop( 'disabled', false );
        $('#programa-comment-content_type-object_id-group textarea').prop( 'disabled', false );
      })

      moveInlines('#programa-contacto-content_type-object_id-group','#content-main>form>div>fieldset:nth-child(2)')
      moveInlines('#programa-grupoactor-content_type-object_id-group','#content-main>form>div>fieldset:nth-child(2)')
      //Triggers rename in case of validation error whilst trying to save
      if ($(".errornote").length) {
          $(".field-propuesta_vinculada select").trigger("change");
      }
    });
  })(django.jQuery);
  