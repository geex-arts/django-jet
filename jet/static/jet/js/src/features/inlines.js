var $ = require('jquery');

var Inline = function($inline) {
    this.$inline = $inline;
};

Inline.prototype = {
    initSelectsOnAddRow: function($inline) {
        $inline.find('.add-row a').on('click', function() {
            $inline.find('.inline-related:not(.empty-form)').last().find('select').trigger('select:init');
        });
    },
    run: function() {
        var $inline = this.$inline;

        try {
            this.initSelectsOnAddRow($inline);
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
