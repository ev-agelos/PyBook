function deleteBookmark() {
    fetch('/api/v1/bookmarks/' + this.dataset.bookmarkId, {
        method: 'DELETE'
    }).then(response => {
        if (response.status == 204){
            return {message: 'Bookmark deleted'}
        }else {
            return response.json()
        }
    }).then(data => M.toast({html: data['message']}))
};

function passBookmarkId() {
    this.el.querySelector("a.waves-green").dataset.bookmarkId = this._openingTrigger.dataset.bookmarkId
};

document.addEventListener('DOMContentLoaded', () => {
    let deleteModal = document.getElementById("deleteModal");
    M.Modal.getInstance(deleteModal).options.onOpenStart = passBookmarkId;

    let yesButton = deleteModal.querySelector("a.waves-green");
    yesButton.addEventListener('click', deleteBookmark);
})
