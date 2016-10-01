var $ = require('jquery');
var CompactInline = require('./compact-inline');

var Inline = function($inline) {
    this.$inline = $inline;
};

Inline.prototype = {
    initAddRow: function($inline) {
        $inline.find('.add-row a').on('click', function() {
            var $inlineItem = $inline.find('.inline-related:not(.empty-form)').last();
            $inline.trigger('inline-group-row:added', [$inlineItem]);
        });
    },
    run: function() {
        var $inline = this.$inline;

        try {
            if ($inline.hasClass('compact')) {
                new CompactInline($inline).run();
            }

            this.initAddRow($inline);
        } catch (e) {
            console.error(e, e.stack);
        }

        $inline.addClass('initialized');
    }
};

$(document).ready(function() {
    $('.inline-group').each(function() {
        new Inline($(this)).run();
    });
});
