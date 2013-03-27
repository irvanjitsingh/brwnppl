$(document).ready(function() {

    $('div.vote-buttons img.vote-up').click(function() {

        var id = {{ video.vid }};
        var vote_type = 'up';

        if ($(this).hasClass('selected')) {
            var vote_action = 'recall-vote'
            $.post('/ajax/thread/vote', {id:vid, type:vote_type, action:vote_action}, function(response) {
                if (isInt(response)) {
                    $('img.vote-up').removeAttr('src')
                        .attr('src', 'images/vote-up-off.png')
                        .removeClass('selected');
                    $('div.vote-tally span.num').html(response);
                }
            });
        } else {

            var vote_action = 'vote'
            $.post('/ajax/thread/vote', {id:vid, type:vote_type, action:vote_action}, function(response) {
                if (isInt(response)) {
                    $('img.vote-up').removeAttr('src')
                        .attr('src', 'images/vote-up-on.png')
                        .addClass('selected');
                    $('div.vote-tally span.num').html(response);
                }
            });
        }
    });

    $('div.vote-buttons img.vote-down').click(function() {

        var id = {{ video.vid }};
        var vote_type = 'down';

        if ($(this).hasClass('selected')) {
            var vote_action = 'recall-vote'
            $.post('/ajax/thread/vote', {id:vid, type:vote_type, action:vote_action}, function(response) {
                if (isInt(response)) {
                    $('img.vote-down').removeAttr('src')
                        .attr('src', 'images/vote-down-off.png')
                        .removeClass('selected');
                    $('div.vote-tally span.num').html(response);
                }
            });
        } else {

            var vote_action = 'vote'
            $.post('/ajax/thread/vote', {id:vid, type:vote_type, action:vote_action}, function(response) {
                if (isInt(response)) {
                    $('img.vote-down').removeAttr('src')
                        .attr('src', 'images/vote-down-on.png')
                        .addClass('selected');
                    $('div.vote-tally span.num').html(response);
                }
            });
        }
    });