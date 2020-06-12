function sendVote(bookmark_id, rating_element, vote, method, change) {
    let csrftoken = $('meta[name=csrf-token]').attr('content');

    fetch('/bookmarks/' + encodeURIComponent(bookmark_id) + '/vote', {
        method: method,
        body: JSON.stringify({'vote': vote}),
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (response.ok) {
            rating_element.innerHTML = parseInt(rating_element.innerHTML) + change;
        }
    })
}

function upVoteBookmark() {
    let orange = 'rgb(255, 102, 0)';
    let method = '';
    let change = 0;
    let parentDiv = this.parentElement.parentElement;
    let oppositeVoteLink = $(parentDiv).children()[2].getElementsByTagName('a')[0];
    let bookmark_id = parentDiv.dataset['bookmarkId'];

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
    let orange = 'rgb(255, 102, 0)';
    let method = '';
    let change = 0;
    let parentDiv = this.parentElement.parentElement;
    let oppositeVoteLink = $(parentDiv).children()[0].getElementsByTagName('a')[0];
    let bookmark_id = parentDiv.dataset['bookmarkId'];

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


document.querySelectorAll(".upVoteLink").forEach(function(item) {
    item.addEventListener('click', upVoteBookmark);
});
document.querySelectorAll(".downVoteLink").forEach(function(item) {
    item.addEventListener('click', downVoteBookmark);
});
