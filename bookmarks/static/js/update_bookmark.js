function updateBookmark(bookmark_id) {
    var formData = new FormData(document.getElementById("updateBookmarkForm"));
    var tags = M.Chips.getInstance($('.chips')).chipsData;
    for (i=0; i<tags.length; i++){
        formData.append('tags-' + i, tags[i].tag);
    };

    $.ajax({
        url: '/bookmarks/' + bookmark_id + '/update',
        method: 'PUT',
        data: formData,
        processData: false,
        contentType: false,
    }).always(function(jqXHR, textStatus){
        M.toast({html: jqXHR['message']});
    });
};


document.addEventListener('DOMContentLoaded', function () {
  // prevent form from submitting
  var form = document.getElementById('updateBookmarkForm');
  $(form).on('submit', function(event){
    event.preventDefault();
    updateBookmark($(form).data()['bookmarkId']);
  });
});



$('.chips').chips();
$('.chips-initial').chips({
    data: JSON.parse(document.getElementById('tags').dataset.tags)
});
