document.addEventListener('DOMContentLoaded', function(){
    $('#submitButton').on('click', function(event){
        document.getElementById('card').style.opacity = 0.3;
        document.getElementById('loadingCircle').className += ' active';
    });
})
