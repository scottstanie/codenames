
$(document).ready(function(){
  // CSRF setup for ajax calls
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });


  $('body').on('click', '.choice', function(e) {
    var $target = $(e.currentTarget);
    var winnerId = $target.data('id');
    var loserId = $(choiceIds).not($(winnerId))[0];
    var $posting = $.post('/polls/vote/',
      {winner: winnerId, loser: loserId}
    );
    $posting.done(function(data) {
      console.log(data); window.location.reload();
    });
  });


  // Create page:

  // Hit flickr API for image suggestions
	$("#submit-search").click(function() {
    var keyword = $("#search-text").val();

    $.ajax({type: "POST",
            url: "/polls/imgsearch/" + keyword,
            //data: {
              //id: $("Shareitem").val()
            //},
            success:function(result){
              var urls = result['imgUrls'];
              var images = $(".image-choice");
              var newarr = jQuery.map(images, function(im, idx) {
                im.src = urls[idx];
              });
    }});
  });

  $(".word-card").click(function() {
    // Set only current div active
    $(".word-card").removeClass("active");
    $(this).addClass("active");

  });

  $("#search-text").keyup(function(e) {
    // On hitting enter:
    if (e.keyCode == 13) {
      $("#submit-search").click();
    }
  });

});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
