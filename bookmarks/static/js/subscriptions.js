document.addEventListener('DOMContentLoaded', function(){
    $('#subscriptionCheckbox').on('click', subscription);
});


subscription = function(){
    let username = this.dataset.userUsername;

    if (this.checked){
        fetch('/api/v1/subscriptions/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({'user_id': this.dataset.userId})
        }).then(response => {
            if (response.status == 204){
                return {message: 'Subscribed to ' + username}
            }else {
                return response.json()
            }
        }).then(data => M.toast({html: data['message']}))
    } else {
        fetch('/api/v1/subscriptions/' + this.dataset.userId, {
            method: 'DELETE',
            headers: {'Content-Type': 'application/json'},
        }).then(response => {
            if (response.status == 204){
                return {message: 'Unsubscribed from ' + username}
            }else {
                return response.json()
            }
        }).then(data => M.toast({html: data['message']}))
    }
};
