$( document ).ready(function() {

});
function search_function(){
  //some code
  $.ajax({
        url: "http://54.83.149.27:8000/reco/search",
        type: "get", //send it through get method
        data:{ajaxid:4, search_term:$(".search_text").val()},
        success: function(response) {
        if($('.search_results').length){
            $('.search_results').remove();
        }
        $('.search').append(response);
        },
        error: function(xhr) {
          //Do Something to handle error
        }
    });
}
$(".search_button").click(function(){
    search_function();
});
$('.search_text').bind("enterKey",function(e){
   search_function();
});
$('.search_text').keyup(function(e){
    if(e.keyCode == 13)
    {
        $(this).trigger("enterKey");
    }
});
var liked_movies = [];
$(".search").on("click",".btn-success", function(){
    $(this).addClass("btn-danger").removeClass("btn-success");
    liked_movies.push($(this).attr("data-mid"));
    $(this).html('Remove');
    console.log(liked_movies);
    $('.liked_movies').append($(this).parent().parent());
});
//$(".search").on("click",".btnadd", function(){
    
    //var 
    //if (index >= 0) {
    //    liked_movies.splice( index, 1 );
    //}
//});
$(".search").on("click",".btn-danger", function(){
    $(this).addClass("btn-success").removeClass("btn-danger");
    index = liked_movies.indexOf($(this).attr("data-mid"));
    if (index >= 0) {
        liked_movies.splice( index, 1 );
    }
    $(this).html('Add');
    console.log(liked_movies);
    $(".liked_movies").find("[data-mid='" + $(this).attr("data-mid") + "']").parent().parent().remove();
});
$(".liked_movies").on("click",".btn-danger", function(){
    index = liked_movies.indexOf($(this).attr("data-mid"));
    if (index >= 0) {
        liked_movies.splice( index, 1 );
    }
    console.log(liked_movies);
    $(".liked_movies").find("[data-mid='" + $(this).attr("data-mid") + "']").parent().parent().remove();
});
$('.btnsubmit').click(function(){
    user_liked =[];
    for(var i=0; i<liked_movies.length; i++) { user_liked[i] = parseInt(liked_movies[i], 10); }
    $.ajax({
        url: "http://192.168.0.102:8000/reco/recommendations",
        type: "get", //send it through get method
        data:{ajaxid:5, user_liked:JSON.stringify(user_liked)},
        success: function(response) {
        if($('.recommendation').length){
            $('.recommendation').remove();
        }
        $('.recommendations').append(response);
        },
        error: function(xhr) {
          //Do Something to handle error
        }
    });    
    });
