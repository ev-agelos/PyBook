function sendVote(bookmark_id, rating_element, vote, method, change) {
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajax({
        url: '/bookmarks/' + encodeURIComponent(bookmark_id) + '/vote',
        data: JSON.stringify({'vote': vote}),
        type: method,
        contentType: 'application/json;charset=UTF-8',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (response) {
            //FIXME setting the correct new rating should change depending on response!
            rating_element.innerHTML = parseInt(rating_element.innerHTML) + change;
        },
        error: function (xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

function upVoteBookmark() {
    var orange = 'rgb(255, 102, 0)';
    var method = '';
    var change = 0;
    var parentDiv = this.parentElement.parentElement;
    var oppositeVoteLink = $(parentDiv).children()[2].getElementsByTagName('a')[0];
    var bookmark_id = parentDiv.dataset['bookmarkId'];

    if (this.style.color === orange) {  // Reset vote
        this.style.color = '';
        method = 'DELETE';
        change = -1;
    } else if (oppositeVoteLink.style.color === orange) {  // From down to up
        this.style.color = orange;
        oppositeVoteLink.style.color = '';
        method = 'PUT';
        change = 2;
    } else {  // New upvote
        this.style.color = orange;
        method = 'POST';
        change = 1;
    };

    sendVote(bookmark_id, $(parentDiv).children()[1], 1, method, change);
};

function downVoteBookmark(){
    var orange = 'rgb(255, 102, 0)';
    var method = '';
    var change = 0;
    var parentDiv = this.parentElement.parentElement;
    var oppositeVoteLink = $(parentDiv).children()[0].getElementsByTagName('a')[0];
    var bookmark_id = parentDiv.dataset['bookmarkId'];

    if (this.style.color === orange) {  // Reset vote
        this.style.color = '';
        method = 'DELETE';
        change = 1;
    } else if (oppositeVoteLink.style.color === orange) {  // From up to down
        oppositeVoteLink.style.color = '';
        this.style.color = orange;
        method = 'PUT';
        change = -2;
    } else {  // New downvote
        this.style.color = orange;
        method = 'POST';
        change = -1;
    };
    sendVote(bookmark_id, $(parentDiv).children()[1], -1, method, change);
};
