function suggestTitle(){
    let suggestButton = this;
    // disable the button until request finishes
    suggestButton.className += ' disabled';

    let url = document.getElementById('url').value;

    fetch('/suggest-title?url=' + url).then(response => response.text()).then(title => {
        document.getElementById("titleLabel").className = "active";
        document.getElementById('title').value = title;
        suggestButton.className = suggestButton.className.replace(' disabled', '');
        suggestButton.blur();
    });
};


document.addEventListener('DOMContentLoaded', function(){
  document.getElementById('suggestTitle').addEventListener('click', suggestTitle);
});
