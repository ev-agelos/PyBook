function suggest(){
    var url_box = document.getElementById('url');
    var url = '/suggest-title?url=' + url_box.value;
    $.ajax(httpGetAsync(url, set_title));

}

function set_title(new_title){
    var title_box = document.getElementById('title');
    document.getElementById("titleLabel").className = "active";
    title_box.value = new_title;
}

function httpGetAsync(theUrl, callback){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
}
