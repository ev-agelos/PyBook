subscription = function(){
    var csrftoken = $('meta[name=csrf-token]').attr('content');
    var xmlHttp = new XMLHttpRequest();
    var message = '';
    var element = this;

    if (this.checked){
        action = 'subscribe';
        method = 'POST';
    }else {
        action = 'unsubscribe';
        method = 'DELETE';
    };

    xmlHttp.onreadystatechange = function(){
        if (xmlHttp.readyState == 4){
            if (xmlHttp.status == 201){
                message = 'Subscribed to ' + element.dataset.userUsername;
            }else if (xmlHttp.status == 204){
                message = 'Unsubscribed from ' + element.dataset.userUsername;
            }else {
                console.log(xmlHttp.response);
                message = JSON.parse(xmlHttp.response)['message'];
            };
            Materialize.toast(message, 4000);
        };
    };

    xmlHttp.open(method, '/users/' + this.dataset.userId + '/' + action, true);
    xmlHttp.setRequestHeader('X-CSRFToken', csrftoken);
    xmlHttp.send(null);
};
