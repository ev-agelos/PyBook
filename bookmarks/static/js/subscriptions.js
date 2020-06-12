document.addEventListener('DOMContentLoaded', function(){
    $('#subscriptionCheckbox').on('click', subscription);
});


subscription = function(){
    let csrftoken = $('meta[name=csrf-token]').attr('content');
    let username = this.dataset.userUsername;

    if (this.checked){
        action = 'subscribe';
        method = 'POST';
    }else {
        action = 'unsubscribe';
        method = 'DELETE';
    };

    fetch('/users/' + this.dataset.userId + '/' + action, {
        method: method,
        headers: {'X-CSRFToken': csrftoken}
    }).then(response => {
        if (response.status == 201){
            return {message: 'Subscribed to ' + username}
        }else if (response.status == 204){
            return {message: 'Unsubscribed from ' + username}
        }else {
            return response.json()
        }
    }).then(data => M.toast({html: data['message']}))
};
