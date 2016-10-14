function saveBookmark(id, bookmark_id) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function(){
        var element = document.getElementById('save' + id);
        if (xmlHttp.readyState == 4){
            var response = JSON.parse(xmlHttp.response);
            var icon = 'star';
            if (xmlHttp.status == 200 || xmlHttp.status == 201){
                if (response['message'] == 'unsaved'){
                    var icon = 'star_border';
                }
                element.innerHTML = icon;
            }
            Materialize.toast('Bookmark ' + response['message'], 4000);
        }
    }
    xmlHttp.open("PUT", '/bookmarks/' + bookmark_id + '/save', true);
    xmlHttp.send(null);
};


function deleteBookmark(bookmark_id) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function(){
        if (xmlHttp.readyState == 4){
            if (xmlHttp.status == 204){
                var message = 'Bookmark deleted'
            }else {
                var message = JSON.parse(xmlHttp.response)['message'];
            }
            Materialize.toast(message, 4000);
        }
    }
    xmlHttp.open("DELETE", '/bookmarks/' + bookmark_id, true);
    xmlHttp.send(null);
};
