function updateBookmark(bookmark_id) {
    var xmlHttp = new XMLHttpRequest();
    var formElement = document.getElementById("updateBookmarkForm");
    var formData = new FormData(formElement);
    var tags = $('.chips').material_chip('data');
    for (i=0; i<tags.length; i++){
        formData.append('tags-' + i, tags[i].tag);
    };

    xmlHttp.onreadystatechange = function(){
        if (xmlHttp.readyState == 4){
            if (xmlHttp.status == 200 || xmlHttp.status == 404 || xmlHttp.status == 400 || xmlHttp.status == 409){
                var message = JSON.parse(xmlHttp.response)['message'];
                Materialize.toast(message, 4000);
            }
        }
    }
    xmlHttp.open("PUT", '/bookmarks/' + bookmark_id + '/update', true);
    xmlHttp.send(formData);
};


document.addEventListener('DOMContentLoaded', function () {
  // prevent form from submitting
  var form = document.getElementById('updateBookmarkForm');
  $(form).on('submit', function(event){
    event.preventDefault();
    updateBookmark($(form).data()['bookmarkId']);
  });
});
