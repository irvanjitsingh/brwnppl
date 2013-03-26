$(function() {
    $('div.video.vote').click(function() {
        var id = $(this).parents('div.video').attr('vid');
        var vote_type = $(this).hasClass('up') ? 'up' : 'down';
        if($(this).hasClass('selected')) {
            $.post('/vote/', {id: vid, type: vote_type}, function(json) {
                if(json.success == 'success') {
                    $(vid)
                     .find('div.' + vote_type);
                    $('div.score', id).html(json.score);
                }
            });
        }
        // } else {
        //     $.post('/remove_vote/', {id: id, type: vote_type}, function(json) {
        //         if(json.success == 'success') {
        //             $('#answer_' + id)
        //              .find('img.' + vote_type);
        //              .attr('src', 'vote_' + vote_type + '.png')
        //              .removeClass('selected');
        //             $('div.score', '#answer_' + id).html(json.score);
        //         }
        //     });                
        // }
    });
});