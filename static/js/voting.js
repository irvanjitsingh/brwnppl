$(document).ready(function() {

    $('div.vote-buttons img.vote-up').click(function() {

        var vid = parseInt($("#vid").text());
        var vote_type = 'up';

        if ($(this).hasClass('selected')) {
            var vote_action = 'recall-vote'
            $.post('/vote', {id:vid, type:vote_type, action:vote_action}, function(response) {
                if (isInt(response)) {
                    $('img.vote-up').removeAttr('src')
                        .attr('src', '{{ STATIC_URL }}img/vote-up-off.png')
                        .removeClass('selected');
                    $('div.vote-tally span.num').html(response);
                }
            });
        } else {

            var vote_action = 'vote'
            $.post('/vote', {id:vid, type:vote_type, action:vote_action}, function(response) {
                if (isInt(response)) {
                    $('img.vote-up').removeAttr('src')
                        .attr('src', '{{ STATIC_URL }}img/vote-up-on.png')
                        .addClass('selected');
                    $('div.vote-tally span.num').html(response);
                }
            });
        }
    });

    $('div.vote-buttons img.vote-down').click(function() {

        var vid = parseInt($("#vid").text());
        var vote_type = 'down';

        if ($(this).hasClass('selected')) {
            var vote_action = 'recall-vote'
            $.post('/vote', {id:vid, type:vote_type, action:vote_action}, function(response) {
                if (isInt(response)) {
                    $('img.vote-down').removeAttr('src')
                        .attr('src', '{{ STATIC_URL }}img/vote-down-off.png')
                        .removeClass('selected');
                    $('div.vote-tally span.num').html(response);
                }
            });
        } else {

            var vote_action = 'vote'
            $.post('/vote', {id:vid, type:vote_type, action:vote_action}, function(response) {
                if (isInt(response)) {
                    $('img.vote-down').removeAttr('src')
                        .attr('src', '{{ STATIC_URL }}img/vote-down-on.png')
                        .addClass('selected');
                    $('div.vote-tally span.num').html(response);
                }
            });
        }
    });
});