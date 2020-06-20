function addBookmark(modal) {
    let url = modal.querySelector("#url");
    let title = modal.querySelector("#title");
    let chips = M.Chips.getInstance(modal.querySelector(".chips"));
    let data = {
        url: url.value,
        title: title.value,
        tags: chips.chipsData.map(object => object['tag'])
    };

    fetch('/api/v1/bookmarks/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => {
        if (response.status == 201){
            url.value = '';
            title.value = '';
            chips.chipsData.forEach((tag, i) => {chips.deleteChip(i)});
            M.Modal.getInstance($(modal)).close();
            return {message: 'Bookmark added'};
        } else {
            return response.json();
        }
    }).then(data => {
        if ('message' in data) {
            M.toast({html: data['message']})
        } else {
            M.toast({html: data['status']})
        }
    })
};

function updateBookmark(modal) {
    let url = modal.querySelector("#url");
    let title = modal.querySelector("#title");
    let chips = M.Chips.getInstance(modal.querySelector(".chips"));
    let data = {
        url: url.value,
        title: title.value,
        tags: chips.chipsData.map(object => object['tag'])
    };

    fetch('/api/v1/bookmarks/' + modal.dataset.bookmarkId, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.status == 204){
                return {message: 'Bookmark updated'}
            } else {
                return response.json()
            }
        })
        .then(data => M.toast({html: data['message']}))
};

function emptyModal(modal) {
    modal.querySelector("#url").value = '';
    modal.querySelector("#title").value = '';
    let chips = M.Chips.getInstance(modal.querySelector(".chips"));
    let iterations = chips.chipsData.length;
    for (i=0; i<iterations; i++) {
        chips.deleteChip(0);
    }
}

function prepareForm() {
    emptyModal(this.el);
    let submit = this.el.querySelector("button.waves-green");
    if (this._openingTrigger.id == "editBookmark") {
        submit.innerText = "Update";
        this.el.dataset.bookmarkId = this._openingTrigger.dataset.bookmarkId;
        fetch('/api/v1/bookmarks/' + this.el.dataset.bookmarkId)
            .then(response => response.json())
            .then(bookmark => {
                let url = this.el.querySelector("#url");
                let title = this.el.querySelector("#title");
                url.value = bookmark['url'];
                title.value = bookmark['title'];
                M.updateTextFields();

                let chips = M.Chips.getInstance(this.el.querySelector(".chips"));
                bookmark['tags'].forEach(function(tag, i){
                    chips.addChip({tag: tag['name']});
                });

            });
    } else if (this._openingTrigger.id == "addBookmark"){
        submit.innerText = "Add";
    }
};

function suggestTitle(){
    // disable the button until request finishes
    this.classList.add("disabled");

    let modal = this.closest("#bookmarkFormModal");
    let url = modal.querySelector("#url");
    let title = modal.querySelector("#title");

    fetch('/suggest-title?url=' + url.value).then(response => response.text()).then(data => {
        title.value = data;
        M.updateTextFields();
        this.classList.remove("disabled");
        this.blur();
    });
};


document.addEventListener('DOMContentLoaded', function(){
    document.getElementById('suggestTitle').addEventListener('click', suggestTitle);

    let modal = document.getElementById("bookmarkFormModal");
    M.Modal.getInstance($(modal)).options.onOpenStart = prepareForm;

    let submit = modal.querySelector("button.waves-green");
    modal.querySelector("button.waves-green").addEventListener('click', () => {
        if (submit.innerText == "ADD") {
            addBookmark(modal);
        } else if (submit.innerText == "UPDATE"){
            updateBookmark(modal);
        }
    })
});
