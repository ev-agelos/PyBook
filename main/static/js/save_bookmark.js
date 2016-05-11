function save(id, bookmark_id)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function(){
        var element = document.getElementById(id).getElementsByTagName('li')[0].getElementsByTagName('a')[0];
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
            if (xmlHttp.responseText == 'Saved'){
                var message = 'unsave';
            }else if (xmlHttp.responseText == 'Unsaved'){
                var message = 'save';
            }
            element.innerHTML=message;
        }
    }
    xmlHttp.open("GET", '/bookmarks/save?bookmark_id=' + bookmark_id, true);
    xmlHttp.send(null);
};
