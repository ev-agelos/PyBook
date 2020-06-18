function checkSubscription() {
    let modal = $("#subscribeModal");
    let checkbox = modal.find("#subscriptionCheckbox")[0];
    checkbox.checked = false; // reset before the check

    fetch('/api/v1/subscriptions/', {
        headers: {'Content-Type': 'application/json'},
    })
        .then(response => response.json())
        .then(data => {
            for (let object of data){
                if (object["user"].endsWith('/' + this.dataset.userId)){
                    checkbox.checked = true;
                    break;
                }
            }
            checkbox.dataset.userId = this.dataset.userId;
            checkbox.dataset.username = this.dataset.username;
            M.Modal.getInstance(modal).open();
        })
}

function subscription(){
    let username = this.dataset.username;
    if (this.checked){
        fetch('/api/v1/subscriptions/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({'user_id': this.dataset.userId})
        }).then(response => {
            if (response.status == 204){
                return {message: 'Subscribed to ' + username}
            }else {
                this.checked = false; // reset state
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
                this.checked = true; // reset state
                return response.json()
            }
        }).then(data => M.toast({html: data['message']}))
    }
};

document.querySelectorAll("#usernameLink").forEach(function(item) {
    item.addEventListener('click', checkSubscription);
});

document.addEventListener('DOMContentLoaded', function(){
    $('#subscriptionCheckbox').on('click', subscription);
});

