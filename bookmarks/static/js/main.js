// Initialize sidebar
$(document).ready(function(){$(".button-collapse").sideNav();});

// Show error messages
var count = 0;
while (document.getElementById('errorMessage-' + count) != null){
    var message = document.getElementById("errorMessage-" + count).dataset.message;
    Materialize.toast(message, 3000, 'rounded');
    count ++;
};
