function addBookmark() {
    let form = document.getElementById("addBookmarkForm");
    let formData = new FormData(form);
    let data = Object.fromEntries(formData);
    let chips = M.Chips.getInstance(form.querySelector('.chips'));
    data['tags'] = chips.chipsData.map(object => object['tag'])

    fetch('/api/v1/bookmarks/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => {
        if (response.status == 201){
            form.reset();
            chips.chipsData.forEach(function(tag, i){
                chips.deleteChip(i)
            });
            M.Modal.getInstance($('#addBookmarkModal')).close();
            M.toast({html: 'Bookmark added'});
        } else if (response.status == 400) {
            M.toast({html: 'Invalid form'});
        } else if (response.status == 409) {
            M.toast({html: 'Bookmark already exists'});
        }
    });
};


document.addEventListener('DOMContentLoaded', function(){
    // prevent form from submitting to send Ajax request
    let form = document.getElementById('addBookmarkForm');
    $(form).on('submit', event => {
        event.preventDefault();
        addBookmark();
    });
});


$('.chips').chips();
