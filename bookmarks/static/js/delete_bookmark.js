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
                Materialize.toast('Bookmark deleted', 4000);
            },
            403: function(data){
                Materialize.toast(data.responseJSON['message'], 4000);
            },
            404: function(data){
                Materialize.toast(data.responseJSON['message'], 4000);
            }
        }
    });
};

$(document).ready(function(){
    $('.modal').modal();
});

$('#deleteButton').on('click', deleteBookmark);
