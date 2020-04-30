document.addEventListener('DOMContentLoaded', function(){
    $('#subscriptionCheckbox').on('click', subscription);
});


subscription = function(){
    var csrftoken = $('meta[name=csrf-token]').attr('content');
    var xmlHttp = new XMLHttpRequest();
    var message = '';
    var username = this.dataset.userUsername;

    if (this.checked){
        action = 'subscribe';
        method = 'POST';
    }else {
        action = 'unsubscribe';
        method = 'DELETE';
    };

    $.ajax({
        url: '/users/' + this.dataset.userId + '/' + action,
        method: method,
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        statusCode: {
            201: function(){
                M.toast({html: 'Subscribed to ' + username});
            },
            204: function(data){
                M.toast({html: 'Unsubscribed from ' + username});
            }
        }
    }).fail(function(jqXHR, textStatus){
        M.toast({html: jqXHR['message']});
    });
};
