// For collapsible movie list
var coll = document.getElementsByClassName("collapsible");
var i;

// Sets to expanded on page load
$(document).ready(function(){
        var coll = document.getElementsByClassName("collapsible");
         var i;

         for (i = 0; i < coll.length; i++) {
            var content = coll[i].nextElementSibling;
            content.style.maxHeight = content.scrollHeight + "px";
                }
});

// Toggle functionality
for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
}

// Modal confirm to delete a Movie Jar
$('#confirm-delete').on('show.bs.modal', function(e) {
    $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
});


// Delete media (movie/TV show) Modal -- populates fields
$('#confirm-media-delete').on('show.bs.modal', function(e) {
    //get data-id attribute of the clicked element
    var movie_name = $(e.relatedTarget).data('movie_name');
    var watchlist_name = $(e.relatedTarget).data('watchlist_name');
    //populate the textbox
    $(e.currentTarget).find('input[name="movie_name"]').val(movie_name);
    $(e.currentTarget).find('input[name="watchlist_name"]').val(watchlist_name);
});


// Update media (movie/TV show) Modal -- populates fields
$('#update-media-info').on('show.bs.modal', function(e) {
    //get data-id attribute of the clicked element
    var mp_name = $(e.relatedTarget).data('mp_name');
    $(e.currentTarget).find('input[name="mp_name"]').val(mp_name);
});

// Show Filter Modal on first page load
$(document).ready(function(){
		$("#filter_modal").modal('show');
	});

//  Disable vibe form after first click
$('#vibe_form').submit(function(){
            $(this).find(':input[type=submit]').prop('disabled', true);
            });


// Disable search from after first click
$('#search_form').submit(function(){
            $(this).find(':input[type=submit]').prop('disabled', true);
            });



// Populates invisible fields on vibe selector form
$('#vibe_selector_modal').on('show.bs.modal', function(e) {
    var mp_id = $(e.relatedTarget).data('mp_id');
    $(e.currentTarget).find('input[name="mp_id"]').val(mp_id);

    var show_movie = $(e.relatedTarget).data('show_movie');
    $(e.currentTarget).find('input[name="show_movie"]').val(show_movie);
});



