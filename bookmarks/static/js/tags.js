function fetchTags() {
    let content = this.el.querySelector(".modal-content");
    let html = '';
    fetch('/api/v1/tags/', {
        headers: {'Content-Type': 'application/json'},
    })
        .then(response => response.json())
        .then(data => {
            for (let object of data) {
                html += '<div class="chip">'
                html += `<a href="/bookmarks/?tag=${object['name']}">${object['name']}</a> ${object['count']}`
                html += '</div>'
            }
            content.innerHTML = html;
        })
};

$(document).ready(function(){
    M.Modal.getInstance($("#tagsModal")).options.onOpenStart = fetchTags;
});
