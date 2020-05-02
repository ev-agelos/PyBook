function updateBookmark() {
    var form = document.getElementById("editBookmarkForm");
    var formData = new FormData(form);
    var tags = M.Chips.getInstance(form.querySelector('.chips')).chipsData;
    for (i=0; i<tags.length; i++){
        formData.append('tags-' + i, tags[i].tag);
    };

    $.ajax({
        url: $('#editBookmarkForm').attr('action'),
        method: 'PUT',
        data: formData,
        processData: false,
        contentType: false,
    }).always(function(jqXHR, textStatus){
        M.toast({html: jqXHR['message']});
    });
};


document.addEventListener('DOMContentLoaded', function(){
    // prevent form from submitting to send Ajax request
    var form = document.getElementById('editBookmarkForm');
    $(form).on('submit', event => {
        event.preventDefault();
        updateBookmark();
    });
});


document.querySelectorAll('#editBookmarkLink').forEach(link => {
    link.addEventListener('click', event => {
        event.preventDefault();

        $.ajax({
            url: link.href,
            method: 'GET',
            processData: false,
            contentType: false,
        }).done(function(bookmark, textStatus, jqXHR){
            var form = document.getElementById('editBookmarkForm');
            form.action = '/bookmarks/' + bookmark['id'] + '/update';
            form.elements['title'].value = bookmark['title'];
            form.elements['url'].value = bookmark['url'];

            var chips = M.Chips.getInstance(form.querySelector(".chips"));
            var iterations = chips.chipsData.length;
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


$('.chips').chips();
