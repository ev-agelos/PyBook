function updateBookmark() {
    let form = document.getElementById("editBookmarkForm");
    let formData = new FormData(form);
    let data = Object.fromEntries(formData);
    let tags = M.Chips.getInstance(form.querySelector('.chips')).chipsData;
    data['tags'] = tags.map(object => object['tag'])

    fetch($('#editBookmarkForm').attr('action'), {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.status == 204){
                return {message: 'Bookmark updated'}
            } else {
                return response.json()
            }
        })
        .then(data => M.toast({html: data['message']}))
};


document.addEventListener('DOMContentLoaded', function(){
    // prevent form from submitting to send Ajax request
    let form = document.getElementById('editBookmarkForm');
    $(form).on('submit', event => {
        event.preventDefault();
        updateBookmark();
    });
});


document.querySelectorAll('#editBookmarkLink').forEach(link => {
    link.addEventListener('click', event => {
        event.preventDefault();

        fetch(link.href)
            .then(response => response.json())
            .then(bookmark => {
                let form = document.getElementById('editBookmarkForm');
                form.action = '/api/v1/bookmarks/' + bookmark['id'];
                form.elements['title'].value = bookmark['title'];
                form.elements['url'].value = bookmark['url'];

                let chips = M.Chips.getInstance(form.querySelector(".chips"));
                let iterations = chips.chipsData.length;
                for (i=0; i<iterations; i++) {
                    chips.deleteChip(0);
                }
                bookmark['tags'].forEach(function(tag, i){
                    chips.addChip({tag: tag['name']});
                });

                M.updateTextFields();
                M.Modal.getInstance($('#editBookmarkModal')).open();
            })
    })
});
