$(document).ready(function () {
    $('.seen').click(function (event) {
        var movie_id = $(this).attr('name');
        $.post('/watchfilm/seen/',{movie_id:movie_id},function (data) {
            if(data){
                window.location='/watchfilm/login/';
            }
            else {
                this.disabled = true;
            }
        })
    });
    $('.add_to_list').click(function (event) {
        var movie_id = $(this).attr('name');
        $.post('/watchfilm/add_to_list/',{movie_id:movie_id},function (data) {
            if(data){
                window.location='/watchfilm/login/';
            }
            else {
                this.disabled = true;
            }
        })
    });
});
