function updateProfile() {
    let form = document.getElementById('profileForm');
    let formData = new FormData(form);
    let data = Object.fromEntries(formData);
    let userId = document.getElementById('profileButton').dataset.userId;

    fetch('/api/v1/users/' + userId, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.status == 204){
                return {message: 'Profile updated'}
            } else {
                return response.json()
            }
        })
        .then(data => {
            if ('errors' in data) {
                M.toast({html: JSON.stringify(data['errors']['json'])})
            } else if ('message' in data) {
                M.toast({html: data['message']})
            }
        })
}

function changePassword() {
    let form = document.getElementById('passwordChangeForm');
    let formData = new FormData(form);
    let data = Object.fromEntries(formData);
    let userId = document.getElementById('profileButton').dataset.userId;

    fetch('/api/v1/users/' + userId, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.status == 204){
                return {message: 'Password succesfully changed'}
            } else {
                return response.json()
            }
        })
        .then(data => {
            if ('errors' in data) {
                M.toast({html: JSON.stringify(data['errors']['json'])})
            } else if ('message' in data) {
                M.toast({html: data['message']})
            }
        })

}

function populateProfileForm() {
    fetch('/api/v1/users/' + this.dataset.userId)
        .then(response => response.json())
        .then(user => {
            let form = document.getElementById('profileForm');
            form.elements['username'].value = user['username'];
            form.elements['email'].value = user['email'];
            M.updateTextFields();
        })
}

document.addEventListener('DOMContentLoaded', function(){
    $('#profileButton').on('click', populateProfileForm);
    let profileForm = document.getElementById('profileForm');
    $(profileForm).on('submit', event => {
        event.preventDefault();
        updateProfile();
    });
    let passwordChangeForm = document.getElementById('passwordChangeForm');
    $(passwordChangeForm).on('submit', event => {
        event.preventDefault();
        changePassword();
    });
});

$(document).ready(function(){
    $('.tabs').tabs();
});
