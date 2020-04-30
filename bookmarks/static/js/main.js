// Initialize sidebar
$(document).ready(function(){$('.sidenav').sidenav();});

// Initialize dropdowns
$('.dropdown-trigger').dropdown();

// Show error messages
var count = 0;
while (document.getElementById('errorMessage-' + count) != null){
    var message = document.getElementById("errorMessage-" + count).dataset.message;
    M.toast({html: message, displayLength: 3000, classes: 'rounded'});
    count ++;
};
