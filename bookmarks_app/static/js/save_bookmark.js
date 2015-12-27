function save(bookmark_id)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function(){
        var element = document.getElementById('save');
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            $('#save')[0].innerHTML="unsave";
    }
    xmlHttp.open("GET", 'bookmarks/save?bookmark_id=' + bookmark_id, true);
    xmlHttp.send(null);
};
