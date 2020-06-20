// Initialize sidebar
$(document).ready(() => {
    $('.sidenav').sidenav();
});

// Initialize dropdowns
$('.dropdown-trigger').dropdown();

// Initialize modals
$('.modal').modal();

// Initialize chips
$('.chips').chips();

// Show error messages
let count = 0;
while (document.getElementById('errorMessage-' + count) != null){
    let message = document.getElementById("errorMessage-" + count).dataset.message;
    M.toast({html: message, displayLength: 3000, classes: 'rounded'});
    count ++;
};
