sendSaveRequest = function(method, bookmark_id, action){
    let csrftoken = $('meta[name=csrf-token]').attr('content');

    fetch('/bookmarks/' + bookmark_id + '/' + action, {
        method: method,
        headers: {'X-CSRFToken': csrftoken}
    }).then(response => {
        if (response.status == 201){
            M.toast({html: 'Bookmark saved'});
        }else if (response.status == 204){
            M.toast({html: 'Bookmark un-saved'});
        }
    })
};


handleFavouriting = function(){
    let method, action, new_icon_html;
    if (this.firstElementChild.innerHTML == 'star'){
        method = 'DELETE';
        action = 'unsave';
        new_icon_html = 'star_border';
    }else{
        method = 'POST';
        action = 'save';
        new_icon_html = 'star';
    };
    sendSaveRequest(method, this.dataset.bookmarkId, action);
    this.firstElementChild.innerHTML = new_icon_html;
};

document.querySelectorAll(".saveIcon").forEach(function(item) {
    item.addEventListener('click', handleFavouriting);
});
