function updateBookmark(bookmark_id) {
    var formElement = document.getElementById("updateBookmarkForm");
    var formData = new FormData(formElement);
    var xmlHttp = new XMLHttpRequest();

    xmlHttp.onreadystatechange = function(){
        if (xmlHttp.readyState == 4){
            if (xmlHttp.status == 200 || xmlHttp.status == 404 || xmlHttp.status == 400 || xmlHttp.status == 409){
                var message = JSON.parse(xmlHttp.response)['message'];
                Materialize.toast(message, 4000);
            }
        }
    }
    xmlHttp.open("PUT", '/bookmarks/' + bookmark_id + '/update', true);
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
  var form = document.getElementById('updateBookmarkForm');
  $(form).on('submit', function(){
    event.preventDefault();
    updateBookmark($(form).data()['bookmarkId']);
  });
});
