(function ($) {
  //Disables editing on comment bodies that have content
  function disabledCommentBodyEditing() {
    console.log('Diableng edit on comment bodies with content')  
    $('#programa-comment-content_type-object_id-group textarea').each(function () {
      if ($(this).text()!==""){
        $(this).prop( 'disabled', true );
        $(this).parent().parent().parent().slideUp();
      }
    })
  }
  $(document).ready(function () {
    console.log("Coparte Edit");
    disabledCommentBodyEditing()
    $('#programa-comment-content_type-object_id-group select').prop( 'disabled', true );
    $('.submit-row input').click(function(){
      $('#programa-comment-content_type-object_id-group select').prop( 'disabled', false );
      $('#programa-comment-content_type-object_id-group textarea').prop( 'disabled', false );
    })
  });
})(django.jQuery);
