function sendVote(bookmark_id, vote, loop_index){
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    });
   $.ajax({
        url: '/bookmarks/' + bookmark_id + '/vote',
        data: JSON.stringify({'vote': vote}),
        type: 'POST',
        contentType: 'application/json;charset=UTF-8',
        success: function(new_rating){
            $('#' + loop_index).html(new_rating);
        },
        error: function(xhr,errmsg,err){
            console.log(xhr.status + ": " + xhr.responseText);
        }
   });
}

function vote(loop_index, bookmark_id, vote){
    var orange = 'rgb(255, 102, 0)';
    var upvote = document.getElementById("up_vote" + loop_index);
    var downvote = document.getElementById("down_vote" + loop_index);

    if (vote === 1 && upvote.style.background == orange){
        upvote.style.background = '';
        sendVote(bookmark_id, 0, loop_index);
    }else if (vote === 1){
        upvote.style.background = orange; 
        if (downvote.style.background == orange){
            downvote.style.background = '';
        }
        sendVote(bookmark_id, 1, loop_index);
    }else if (vote === -1 && downvote.style.background == orange){
        downvote.style.background = '';
        sendVote(bookmark_id, 0, loop_index);
    }else if (vote === -1){
        downvote.style.background = orange; 
        if (upvote.style.background == orange){
            upvote.style.background = '';
        }
        sendVote(bookmark_id, -1, loop_index);
    }
}
