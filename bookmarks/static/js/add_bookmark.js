function addBookmark() {
    var bookmarkForm = document.getElementById("addBookmarkForm");
    var formData = new FormData(bookmarkForm);
    var xmlHttp = new XMLHttpRequest();

    xmlHttp.onreadystatechange = function(){
        if (xmlHttp.readyState == 4){
            if (xmlHttp.status == 201){
                var message = 'Bookmark added';
            }else if (xmlHttp.status == 409){
                var message = 'Bookmark already exists';
            }else if (xmlHttp.status == 400){
                var message = 'Invalid form';
            }else {
                var message = 'Internal server error';
            }
            Materialize.toast(message, 4000);
        }
    }
    xmlHttp.open("POST", '/bookmarks/add', true);
    xmlHttp.send(formData);
};

function setCategory() {
  document.getElementById("categoryLabel").className = "active";  // set label active for the effect
  category_select = document.getElementById('category_list')
  document.getElementById("category").value = category_select.value;  // set the category on the text field
};


document.addEventListener('DOMContentLoaded', function () {
  $('select').material_select();  // initialization of material select
  category_select = document.getElementById('category_list')
  $(category_select).on('change', setCategory);
});


document.addEventListener('DOMContentLoaded', function () {
  // prevent form from submitting
  var form = document.getElementById('addBookmarkForm');
  $(form).on('submit', function(){
    event.preventDefault();
    addBookmark();
  });
});
