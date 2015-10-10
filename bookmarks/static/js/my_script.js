function sendVote(bookmark_title, vote, loop_index){
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    });
   $.ajax({
        url: '/bookmarks/' + bookmark_title + '/vote',
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

function vote(loop_index, bookmark_title, vote){
    var orange = 'rgb(255, 102, 0)';
    var upvote = document.getElementById("up_vote" + loop_index);
    var downvote = document.getElementById("down_vote" + loop_index);

    if (vote === 1 && upvote.style.color == orange){
        upvote.style.color = '';
        sendVote(bookmark_title, 0, loop_index);
    }else if (vote === 1){
        upvote.style.color = orange; 
        if (downvote.style.color == orange){
            downvote.style.color = '';
        }
        sendVote(bookmark_title, 1, loop_index);
    }else if (vote === -1 && downvote.style.color == orange){
        downvote.style.color = '';
        sendVote(bookmark_title, 0, loop_index);
    }else if (vote === -1){
        downvote.style.color = orange; 
        if (upvote.style.color == orange){
            upvote.style.color = '';
        }
        sendVote(bookmark_title, -1, loop_index);
    }
}
