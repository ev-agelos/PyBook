function suggestTitle(){
    var suggestButton = this;
    // disable the button until request finishes
    suggestButton.className += ' disabled';

    var url = document.getElementById('url').value;

    $.ajax({
        url: '/suggest-title?url=' + url,
        method: 'GET',
    }).done(function(data){
        document.getElementById("titleLabel").className = "active";
        document.getElementById('title').value = data;
    }).always(function(jqXHR, textStatus){
        suggestButton.className = suggestButton.className.replace(' disabled', '');
        suggestButton.blur();
    });
};


document.addEventListener('DOMContentLoaded', function(){
  document.getElementById('suggestTitle').addEventListener('click', suggestTitle);
});
