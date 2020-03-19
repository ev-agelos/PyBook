sendSaveRequest = function(method, bookmark_id, action){
    var xmlHttp = new XMLHttpRequest();
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    xmlHttp.onreadystatechange = function(){
        if (xmlHttp.readyState == 4){
            if (xmlHttp.status == 201){
                Materialize.toast('Bookmark saved', 4000);
            }else if (xmlHttp.status == 204){
                Materialize.toast('Bookmark unsaved', 4000);
            }
        }
    }
    xmlHttp.open(method, '/bookmarks/' + bookmark_id + '/' + action, true);
    xmlHttp.setRequestHeader('X-CSRFToken', csrftoken);
    xmlHttp.send(null);
};


handleFavouriting = function(){
    if (this.innerHTML == 'star'){
        var method = 'DELETE';
        var action = 'unsave';
        var new_icon_html = 'star_border';
    }else{
        var method = 'POST';
        var action = 'save';
        var new_icon_html = 'star';
    };
    sendSaveRequest(method, this.dataset.bookmarkId, action);
    this.innerHTML = new_icon_html;
};

$('#saveIcon').on('click', handleFavouriting);
