function addBookmark() {
    var form = document.getElementById("addBookmarkForm");
    var formData = new FormData(form);
    var chips = M.Chips.getInstance(form.querySelector('.chips'));
    for (i=0; i<chips.chipsData.length; i++){
        formData.append('tags-' + i, chips.chipsData[i].tag);
    };

    $.ajax({
        url: '/bookmarks/add',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        statusCode: {
            201: function(){
                form.reset();
                chips.chipsData.forEach(function(tag, i){
                    chips.deleteChip(i)
                });
                M.Modal.getInstance($('#addBookmarkModal')).close();
                M.toast({html: 'Bookmark added'});
            },
            400: function(){
                M.toast({html: 'Invalid form'});
            },
            409: function(){
                M.toast({html: 'Bookmark already exists'});
            }
        }
    })
};


document.addEventListener('DOMContentLoaded', function(){
    // prevent form from submitting to send Ajax request
    var form = document.getElementById('addBookmarkForm');
    $(form).on('submit', event => {
        event.preventDefault();
        addBookmark();
    });
});


$('.chips').chips();
