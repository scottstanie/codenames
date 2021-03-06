
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
    var requestUser = $('#user-info').data('request-user');
    if (requestUser != 'None') {
        // On the timer, check if they have games waiting every 60 sec
        setInterval(function() {
            checkWaiting(requestUser);
        }, 60000);
    };
    checkWaiting(requestUser);

    $('#submit-pass').click(function(e) {
        if(!confirm('Sure you want to pass?')) {
            return false;
        }
        var $teamColor = $('#currentTeam').data('team-color');
        var game_id = location.pathname.split('/')[2];
        var $player = $('#player').text();
        var $clueNumber = $('#clue-number').text();
        var $posting = $.post(
            '/guess/', {
                    wordId: null,
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
        if ($wordChoice.data('chosen') === "True") {
            alert("Can't choose the same word twice!");
            return false;
        }
        var wordId = $wordChoice.attr('id');
        var $teamColor = $('#currentTeam').data('team-color');
        var game_id = location.pathname.split('/')[2];
        var $player = $('#player').text();
        var $clueNumber = $('#clue-number').text();
        var $posting = $.post(
            '/guess/', {
                    wordId: wordId,
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
    var $chosenCards = $('.word-card[data-chosen="True"]');
    $.map($chosenCards, function(card) {
        $(card).addClass("chosen");
        showColor(card);
    });

    $(".word-card").click(function() {
        // Set only current div active
        $(".word-card").removeClass("active");
        $(this).addClass("active");

    });

    $("#clue-text").keyup(function(e) {
        // On hitting enter:
        if (e.keyCode === 13) {
            $("#submit-clue").click();
        }
    });

    $('#submit-clue').click(function(e) {
        var $cardCount = $('#card-count').find(":selected").text();
        if($cardCount === '0') {
            if(!confirm('Sure you want a word 0 clue?')) {
                return false;
            }
        }
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

    var $gameInfo = $('#game-info');
    var gameActive = $gameInfo.data('active');
    var currentPlayer = $gameInfo.data('current-player');
    var isGiver = $gameInfo.data('is-giver');

    if (currentPlayer != requestUser) {
        hideInputs(true, true);
    };

    // For the users that are givers in this game, show all card colors
    if (isGiver === "True") {
        $.map($('.word-card'), showColor);
        // Hide the guessing buttons for givers
        hideInputs(false, true);
    } else {
        // Hide the giving buttons for guessers
        hideInputs(true, false);
    };


    // Once the game is over, show the color map
    if (gameActive === "False") {
        $.map($('.word-card'), showColor);
        hideInputs(true, true);
    };


    // Refresh page on inactivity
    var currentTime = new Date().getTime();
    $(document.body).bind("mousemove touchmove keypress", function(e) {
        currentTime = new Date().getTime();
    });

    // Add comment
    $('#addCommentBtn').click(function(e) {
        e.preventDefault();
        addComment();
    })
    $('.removeCommentBtn').click(function() {
        if(!confirm('Delete this comment?')) {
            return false;
        }
        var $commentId = $(this).data('comment-id');
        removeComment($commentId);
    })

});

// Check if there are games waiting
function checkWaiting(requestUser) {
    $.ajax({
        type: 'GET',
        url: '/waiting/' + requestUser,
        success: function(result) {
            if(result['waitingOnYou']) {
                setWaiting();
            };
        },
    });
}

// Change the 'My Games' in navbar to red if user has games waiting
function setWaiting() {
    $('#my-games').css({
        "border": "solid red 2px",
        "color": "red"
    });
    var $title = $('title');
    if ($title.text() === 'Codenames') {
        $title.prepend('(1) ');
    }
}

// Highlight any that have been chosen
function showColor(card) {
    $(card).css({
        "color": "white"
    })
    $(card).css('background-color', function() {
        return $(this).data('color');
    })
}

// Remove input buttons if it's not your turn
function hideInputs(giving, guessing) {
    // giving: hide the '.giving' input buttons
    // guessing: hide the '.guessing' input buttons
    function hide(classString) {
        $(classString).map(function() {
            $(this).css('display', 'none');
        });
    }
    if (giving) hide('.inputs.giving');
    if (guessing) hide('.inputs.guessing');
}

function addComment() {
    var game_id = location.pathname.split('/')[2];
    var $commentText = $('#commentText').val();
    var $teamColor = $('#currentTeam').data('team-color');
    var $posting = $.post(
        '/comment/', {
            game_id: game_id,
            text: $commentText,
            color: $teamColor
        }
    );
    $posting.done(function(data) {
        window.location.reload();
    });
}

function removeComment(commentId) {
    var $posting = $.post('/comment/' + commentId);
    $posting.done(function(data) {
        window.location.reload();
    });
}

function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
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
