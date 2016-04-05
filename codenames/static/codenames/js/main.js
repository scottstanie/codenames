
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


  $('body').on('click', '#submit', function(e) {
    var $wordChoice = $('.active.word-card');
    var text = $wordChoice.text();
    var color = $wordChoice.data('color');
    var game_id = location.pathname.split('/')[2];
    var $posting = $.post(
      '/move/', 
      {text: text, color: color, game_id: game_id} 
    );
    $posting.done(function(data) {
      window.location.reload();
    });
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
