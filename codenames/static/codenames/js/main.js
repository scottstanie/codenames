
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


  $('#submit-pass').click(function(e) {
    var $teamColor = $('#currentTeam').data('team-color');
    var game_id = location.pathname.split('/')[2];
    var $player = $('#player').text();
    var $clueNumber = $('#clue-number').text();
    var $posting = $.post(
      '/guess/', {
          text: null,
          teamColor: $teamColor,
          game_id: game_id,
          player: $player,
          clueNumber: $clueNumber,
      }
    );
    $posting.done(function(data) {
      window.location.reload();
    });
  });

  $('#submit-guess').click(function(e) {
    var $wordChoice = $('.active.word-card');
    var text = $wordChoice.text();
    var $teamColor = $('#currentTeam').data('team-color');
    var game_id = location.pathname.split('/')[2];
    var $player = $('#player').text();
    var $clueNumber = $('#clue-number').text();
    var $posting = $.post(
      '/guess/', {
          text: text,
          teamColor: $teamColor,
          game_id: game_id,
          player: $player,
          clueNumber: $clueNumber,
      }
    );
    $posting.done(function(data) {
      window.location.reload();
    });
  });

  // Highlight any that have been chosen
  $('.word-card[data-chosen="True"]').addClass("chosen").css('background-color', function() {
    return $(this).data('color');
  })

  $(".word-card").click(function() {
    // Set only current div active
    $(".word-card").removeClass("active");
    $(this).addClass("active");

  });

  $("#clue-text").keyup(function(e) {
    // On hitting enter:
    if (e.keyCode == 13) {
      $("#submit-clue").click();
    }
  });

  $('#submit-clue').click(function(e) {
    var $cardCount = $('#card-count').find(":selected").text();
    var $clueText = $('#clue-text').val();
    var $player = $('#player').text();
    if($clueText === "") {
      alert("Please enter a clue!");
      return false
    }
    var game_id = location.pathname.split('/')[2];
    var $posting = $.post(
      '/give/', {
        text: $clueText,
        count: $cardCount,
        game_id: game_id,
        player: $player
      }
    );
    $posting.done(function(data) {
      window.location.reload();
    });
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
