function updateBookmark(bookmark_id) {
    var formData = new FormData(document.getElementById("updateBookmarkForm"));
    var tags = $('.chips').material_chip('data');
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
        Materialize.toast(jqXHR['message'], 4000);
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



$('.chips').material_chip();
$('.chips-initial').material_chip({
    data: JSON.parse(document.getElementById('tags').dataset.tags)
});
