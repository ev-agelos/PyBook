function deleteBookmark() {
    let csrftoken = $('meta[name=csrf-token]').attr('content');

    fetch('/bookmarks/' + this.dataset.bookmarkId + '/delete', {
        method: 'DELETE',
        headers: {'X-CSRFToken': csrftoken}
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
