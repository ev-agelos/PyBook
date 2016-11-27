function deleteBookmark() {
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
    xmlHttp.open("DELETE", '/bookmarks/' + this.dataset.bookmarkId + '/delete', true);
    xmlHttp.send(null);
};
