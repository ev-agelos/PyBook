function addBookmark() {
    var xmlHttp = new XMLHttpRequest();
    var bookmarkForm = document.getElementById("addBookmarkForm");
    var formData = new FormData(bookmarkForm);
    var tags = $('.chips').material_chip('data');
    for (i=0; i<tags.length; i++){
        formData.append('tags-' + i, tags[i].tag);
    };

    xmlHttp.onreadystatechange = function(){
        if (xmlHttp.readyState == 4){
            if (xmlHttp.status == 201){
                var message = 'Bookmark added';
            }else if (xmlHttp.status == 409){
                var message = 'Bookmark already exists';
            }else if (xmlHttp.status == 400){
                var message = 'Invalid form';
            }else {
                var message = 'Internal server error';
            }
            Materialize.toast(message, 4000);
        }
    }
    xmlHttp.open("POST", '/bookmarks/add', true);
    xmlHttp.send(formData);
};


document.addEventListener('DOMContentLoaded', function(){
  // prevent form from submitting to send Ajax request
  var form = document.getElementById('addBookmarkForm');
  $(form).on('submit', function(){
    event.preventDefault();
    addBookmark();
  });
});
