function deleteBookmark() {
    fetch('/api/v1/bookmarks/' + this.dataset.bookmarkId, {
        method: 'DELETE',
        credentials: 'same-origin'
    }).then(response => {
        if (response.status == 204){
            return {message: 'Bookmark deleted'}
        }else {
            return response.json()
        }
    }).then(data => M.toast({html: data['message']}))
};

$(document).ready(function(){
    $('.modal').modal();
});

document.querySelectorAll(".deleteButton").forEach(function(item) {
    item.addEventListener('click', deleteBookmark);
});
