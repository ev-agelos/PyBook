sendSaveRequest = function(method, bookmark_id, action){
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajax({
        url: '/bookmarks/' + bookmark_id + '/' + action,
        method: method,
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        statusCode: {
            201: function(){
                Materialize.toast('Bookmark saved', 4000);
            },
            204: function(data){
                Materialize.toast('Bookmark un-saved', 4000);
            }
        }
    });
};


handleFavouriting = function(){
    if (this.firstElementChild.innerHTML == 'star'){
        var method = 'DELETE';
        var action = 'unsave';
        var new_icon_html = 'star_border';
    }else{
        var method = 'POST';
        var action = 'save';
        var new_icon_html = 'star';
    };
    sendSaveRequest(method, this.dataset.bookmarkId, action);
    this.firstElementChild.innerHTML = new_icon_html;
};

document.querySelectorAll(".saveIcon").forEach(function(item) {
    item.addEventListener('click', handleFavouriting);
});
