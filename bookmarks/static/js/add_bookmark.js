function addBookmark() {
    let form = document.getElementById("addBookmarkForm");
    let formData = new FormData(form);
    let chips = M.Chips.getInstance(form.querySelector('.chips'));
    for (i=0; i<chips.chipsData.length; i++){
        formData.append('tags-' + i, chips.chipsData[i].tag);
    };

    fetch('/bookmarks/add', {
        method: 'POST',
        body: formData
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
