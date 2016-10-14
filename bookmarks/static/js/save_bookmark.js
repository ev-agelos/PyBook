function save(id, bookmark_id)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function(){
        var element = document.getElementById('save' + id);
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
            if (xmlHttp.responseText == 'Saved'){
                var message = 'star';
                var info_message = 'Bookmark saved!';
            }else if (xmlHttp.responseText == 'Unsaved'){
                var message = 'star_border';
                var info_message = 'Bookmark unsaved'
            }
            Materialize.toast(info_message, 4000);
            element.innerHTML= message;
        }
    }
    xmlHttp.open("GET", '/bookmarks/save?bookmark_id=' + bookmark_id, true);
    xmlHttp.send(null);
};
