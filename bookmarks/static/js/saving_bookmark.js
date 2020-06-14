handleFavouriting = function(){
    let new_icon_html;

    if (this.firstElementChild.innerHTML == 'star'){
        fetch('/api/v1/favourites/' + this.dataset.bookmarkId, {
            method: 'DELETE',
            credentials: 'same-origin'
        }).then(response => {
            if (response.status == 204){
                M.toast({html: 'Bookmark un-saved'});
            }
        })
        new_icon_html = 'star_border';
    }else{
        fetch('/api/v1/favourites/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'bookmark_id': parseInt(this.dataset.bookmarkId)}),
        }).then(response => {
            if (response.status == 201){
                M.toast({html: 'Bookmark saved'});
            }
        })
        new_icon_html = 'star';
    };

    this.firstElementChild.innerHTML = new_icon_html;
};

document.querySelectorAll(".saveIcon").forEach(function(item) {
    item.addEventListener('click', handleFavouriting);
});
