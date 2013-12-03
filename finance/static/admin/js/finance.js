(function($){
    $(document).ready(function($) {
        $("button.delete").click(function(){
            var pk = $(this).val();
            var $tr_parent = $(this).parents('tr');
            $.ajax({
                'url': '/news/delete/',
                'type': 'POST',
                'data': {'pk': pk },
                'cache': false,
                'success': function(response){
                    if(response.success){
                        $tr_parent.remove();
                    }
                },
                'dataType': 'json'
            });
        });
    })
})(django.jQuery);
