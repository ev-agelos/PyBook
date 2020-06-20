function deleteVote(vote_id){
    fetch('/api/v1/votes/' + vote_id, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
}

function putVote(vote_id, data) {
    fetch('/api/v1/votes/' + vote_id, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
}

async function postVote(data) {
    const response = await fetch('/api/v1/votes/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        return response.headers.get('Location');
    } else {
        return response.json();
    }
}

function upVoteBookmark() {
    let vote_id = this.parentElement.parentElement.dataset['voteId'];
    let rating = this.parentElement.parentElement.querySelector("#ratingNumber");
    let downVoteLink = this.parentElement.parentElement.querySelector(".downVoteLink");

    if (this.classList.contains("grey")) {  // Cancel upvote
        // reset this
        this.classList.remove("grey");
        this.classList.remove("lighten-2");
        this.classList.add("white");

        deleteVote(vote_id);
        delete this.parentElement.parentElement.dataset.voteId;
        rating.innerHTML = parseInt(rating.innerHTML) - 1;
    } else if (downVoteLink.classList.contains("grey")) {  // Is downvoted
        // highlight this
        this.classList.remove("white");
        this.classList.add("grey");
        this.classList.add("lighten-2");
        // reset opposite
        downVoteLink.classList.remove("grey");
        downVoteLink.classList.remove("lighten-2");
        downVoteLink.classList.add("white");

        putVote(vote_id, {'direction': 1});
        rating.innerHTML = parseInt(rating.innerHTML) + 2;
    } else {  // New upvote
        let bookmark_id = this.parentElement.parentElement.dataset['bookmarkId'];
        postVote({'bookmark_id': bookmark_id, 'direction': 1})
            .then(data => {
                if (typeof data === 'string') {
                    this.classList.remove("white");
                    this.classList.add("grey");
                    this.classList.add("lighten-2");
                    rating.innerHTML = parseInt(rating.innerHTML) + 1;
                    let url_parts = data.split("/");
                    let vote_id = url_parts[url_parts.length - 1];
                    this.parentElement.parentElement.dataset.voteId = vote_id;
                } else {
                    M.toast({html: data['status']});
                }
            });
    };
};

function downVoteBookmark(){
    let vote_id = this.parentElement.parentElement.dataset['voteId'];
    let rating = this.parentElement.parentElement.querySelector("#ratingNumber");
    let upVoteLink = this.parentElement.parentElement.querySelector(".upVoteLink");

    if (this.classList.contains("grey")) {  // Cancel upvote
        // reset this
        this.classList.remove("grey");
        this.classList.remove("lighten-2");
        this.classList.add("white");

        deleteVote(vote_id);
        delete this.parentElement.parentElement.dataset.voteId;
        rating.innerHTML = parseInt(rating.innerHTML) + 1;
    } else if (upVoteLink.classList.contains("grey")) {  // Is upvoted
        // highlight this
        this.classList.remove("white");
        this.classList.add("grey");
        this.classList.add("lighten-2");
        // reset opposite
        upVoteLink.classList.remove("grey");
        upVoteLink.classList.remove("lighten-2");
        upVoteLink.classList.add("white");

        putVote(vote_id, {'direction': -1});
        rating.innerHTML = parseInt(rating.innerHTML) - 2;
    } else {  // New downvote
        let bookmark_id = this.parentElement.parentElement.dataset['bookmarkId'];
        postVote({'bookmark_id': bookmark_id, 'direction': -1})
            .then(data => {
                if (typeof data === 'string') {
                    this.classList.remove("white");
                    this.classList.add("grey");
                    this.classList.add("lighten-2");
                    let url_parts = data.split("/");
                    let vote_id = url_parts[url_parts.length - 1];
                    this.parentElement.parentElement.dataset.voteId = vote_id;
                    rating.innerHTML = parseInt(rating.innerHTML) - 1;
                } else {
                    M.toast({html: data['status']});
                }
            });
    };
};


document.querySelectorAll(".upVoteLink").forEach(function(item) {
    item.addEventListener('click', upVoteBookmark);
});
document.querySelectorAll(".downVoteLink").forEach(function(item) {
    item.addEventListener('click', downVoteBookmark);
});
