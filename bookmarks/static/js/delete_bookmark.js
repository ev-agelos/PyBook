function deleteBookmark() {
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajax({
        url: '/bookmarks/' + this.dataset.bookmarkId + '/delete',
        method: 'DELETE',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        statusCode: {
            204: function(){
                M.toast({html: 'Bookmark deleted'});
            },
            403: function(data){
                M.toast({html: data.responseJSON['message']});
            },
            404: function(data){
                M.toast({html: data.responseJSON['message']});
            }
        }
    });
};

$(document).ready(function(){
    $('.modal').modal();
});

document.querySelectorAll(".deleteButton").forEach(function(item) {
    item.addEventListener('click', deleteBookmark);
});
