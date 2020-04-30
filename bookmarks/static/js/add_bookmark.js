function addBookmark() {
    var formData = new FormData(document.getElementById("addBookmarkForm"));
    var tags = M.Chips.getInstance($('.chips')).chipsData;
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
                M.toast({html: 'Bookmark added'});
            },
            400: function(){
                M.toast({html: 'Invalid form'});
            },
            409: function(){
                M.toast({html: 'Bookmark already exists'});
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


$('.chips').chips();
$('.chips-initial').chips({
    data: JSON.parse(document.getElementById('tags').dataset.tags)
});
