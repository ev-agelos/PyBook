function suggestTitle(){
    var suggestButton = this;
    suggestButton.className += ' disabled';  // disable the button until request finishes
    var url = document.getElementById('url').value;
    var xmlHttp = new XMLHttpRequest();

    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4){
            if (xmlHttp.status == 200){
                document.getElementById("titleLabel").className = "active";
                document.getElementById('title').value = xmlHttp.responseText;
            };
            suggestButton.className = suggestButton.className.replace(' disabled', '');
            suggestButton.blur();
        };
    };
    xmlHttp.open("GET", '/suggest-title?url=' + url, true); // true for asynchronous
    xmlHttp.send(null);
};


document.addEventListener('DOMContentLoaded', function(){
  document.getElementById('suggestTitle').addEventListener('click', suggestTitle);
});
