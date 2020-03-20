function addBookmark() {
    var formData = new FormData(document.getElementById("addBookmarkForm"));
    var tags = $('.chips').material_chip('data');
    for (i=0; i<tags.length; i++){
        formData.append('tags-' + i, tags[i].tag);
    };

    $.ajax({
        url: '/bookmarks/add',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        statusCode: {
            201: function(){
                Materialize.toast('Bookmark added', 4000);
            },
            400: function(){
                Materialize.toast('Invalid form', 4000);
            },
            409: function(){
                Materialize.toast('Bookmark already exists', 4000);
            }
        }
    });
};


document.addEventListener('DOMContentLoaded', function(){
  // prevent form from submitting to send Ajax request
  var form = document.getElementById('addBookmarkForm');
  $(form).on('submit', function(event){
    event.preventDefault();
    addBookmark();
  });
});


$('.chips').material_chip();
$('.chips-initial').material_chip({
    data: JSON.parse(document.getElementById('tags').dataset.tags)
});
