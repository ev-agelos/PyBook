function fetchUsers() {
    console.log(111111)
    let collection = this.el.querySelector(".collection");
    let html = '';
    fetch('/api/v1/users/', {
        headers: {'Content-Type': 'application/json'},
    })
        .then(response => response.json())
        .then(data => {
            for (let object of data) {
                html += '<a href="#!" class="collection-item">'+ object['username'] +'</a>'
            }
            collection.innerHTML = html;
        })
};

$(document).ready(function(){
    M.Modal.getInstance($("#usersModal")).options.onOpenStart = fetchUsers;
});
