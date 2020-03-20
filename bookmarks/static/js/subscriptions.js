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
                Materialize.toast('Subscribed to ' + username, 4000);
            },
            204: function(data){
                Materialize.toast('Unsubscribed from ' + username, 4000);
            }
        }
    }).fail(function(jqXHR, textStatus){
        Materialize.toast(jqXHR['message'], 4000);
    });
};
