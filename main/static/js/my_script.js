function sendVote(bookmark_title, vote, loop_index, up_vote_color, down_vote_color){
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    });
   $.ajax({
        url: '/bookmarks/' + encodeURIComponent(bookmark_title) + '/vote',
        data: JSON.stringify({'vote': vote}),
        type: 'POST',
        contentType: 'application/json;charset=UTF-8',
        success: function(new_rating){
            if (up_vote_color !== undefined){
                var upvote = document.getElementById("up_vote" + loop_index);
                upvote.style.color = up_vote_color;
            }
            if (down_vote_color !== undefined){
                var downvote = document.getElementById("down_vote" + loop_index);
                downvote.style.color = down_vote_color; 
            }
            var total_votes = document.getElementById("total_vote_" + loop_index);
            total_votes.innerHTML="<strong>" + new_rating + "</strong>";
        },
        error: function(xhr,errmsg,err){
            console.log(xhr.status + ": " + xhr.responseText);
        }
   });
}

function vote(loop_index, bookmark_title, vote){
    var orange = 'rgb(255, 102, 0)';
    var upvote = document.getElementById("up_vote" + loop_index);
    var downvote = document.getElementById("down_vote" + loop_index);

    if (vote === 1 && upvote.style.color == orange){
        sendVote(bookmark_title, 0, loop_index, '', null);
    }else if (vote === 1){
        if (downvote.style.color == orange){
        sendVote(bookmark_title, 1, loop_index, orange, '');
        }else{
            sendVote(bookmark_title, 1, loop_index, orange, null);
        }
    }else if (vote === -1 && downvote.style.color == orange){
        sendVote(bookmark_title, 0, loop_index, null, '');
    }else if (vote === -1){
        if (upvote.style.color == orange){
            sendVote(bookmark_title, -1, loop_index, '', orange);
        }else{
            sendVote(bookmark_title, -1, loop_index, null, orange);
        }
    }
}
