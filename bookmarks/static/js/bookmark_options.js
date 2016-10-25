saveBookmark = function(id, bookmark_id) {
    var xmlHttp = new XMLHttpRequest();
    var bookmark = document.getElementById('bookmarkLink' + id);

    xmlHttp.onreadystatechange = function(){
        if (xmlHttp.readyState == 4){
            if (xmlHttp.status == 201){
                bookmark.getElementsByTagName('i')[0].innerHTML = 'star';
                bookmark.onclick = function(){unsaveBookmark(id, bookmark_id)};
                Materialize.toast('Bookmark saved', 4000);
            }
        }
    }
    xmlHttp.open('POST', '/bookmarks/' + bookmark_id + '/save', true);
    xmlHttp.send(null);
};


unsaveBookmark = function(id, bookmark_id) {
    var xmlHttp = new XMLHttpRequest();
    var bookmark = document.getElementById('bookmarkLink' + id);

    xmlHttp.onreadystatechange = function(){
        if (xmlHttp.readyState == 4){
            if (xmlHttp.status == 204){
                bookmark.getElementsByTagName('i')[0].innerHTML = 'star_border';
                bookmark.onclick = function(){saveBookmark(id, bookmark_id)};
                Materialize.toast('Bookmark unsaved', 4000)
            }
        }
    }
    xmlHttp.open('DELETE', '/bookmarks/' + bookmark_id + '/unsave', true);
    xmlHttp.send(null);
};


function addBookmark() {
    var bookmarkForm = document.getElementById("addBookmarkForm");
    var formData = new FormData(bookmarkForm);
    var xmlHttp = new XMLHttpRequest();

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


function deleteBookmark(bookmark_id) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function(){
        if (xmlHttp.readyState == 4){
            if (xmlHttp.status == 204){
                var message = 'Bookmark deleted'
                Materialize.toast(message, 4000);
            }else if (xmlHttp.status == 403 || xmlHttp.status == 404) {
                var message = JSON.parse(xmlHttp.response)['message'];
                Materialize.toast(message, 4000);
            }
        }
    }
    xmlHttp.open("DELETE", '/bookmarks/' + bookmark_id + '/delete', true);
    xmlHttp.send(null);
};


function updateBookmark(bookmark_id) {
    var formElement = document.getElementById("updateBookmarkForm");
    var formData = new FormData(formElement);
    var xmlHttp = new XMLHttpRequest();

    xmlHttp.onreadystatechange = function(){
        if (xmlHttp.readyState == 4){
            if (xmlHttp.status == 200 || xmlHttp.status == 404 || xmlHttp.status == 400 || xmlHttp.status == 409){
                console.log(xmlHttp.response);
                var message = JSON.parse(xmlHttp.response)['message'];
                Materialize.toast(message, 4000);
            }
        }
    }
    xmlHttp.open("PUT", '/bookmarks/' + bookmark_id + '/update', true);
    xmlHttp.send(formData);
};


function suggestTitle(){
    var url = document.getElementById('url').value;
    var xmlHttp = new XMLHttpRequest();

    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
            document.getElementById("titleLabel").className = "active";
            document.getElementById('title').value = xmlHttp.responseText;
        }
    }
    xmlHttp.open("GET", '/suggest-title?url=' + url, true); // true for asynchronous
    xmlHttp.send(null);
};


function setCategory() {
    document.getElementById("categoryLabel").className = "active";
    document.getElementById("category").value = document.getElementById("category_list").value;
};
