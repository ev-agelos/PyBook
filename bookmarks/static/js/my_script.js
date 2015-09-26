function vote(element, bookmark_id, value){
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    });
   $.ajax({
        url: '/vote_bookmark',
        data: {'vote': value, 'bookmark_id': bookmark_id},
        type: 'POST',
        success: function(new_rating){
            $('#' + element).html(new_rating);
        },
        error: function(xhr,errmsg,err){
            console.log(xhr.status + ": " + xhr.responseText);
        }
   });
}
