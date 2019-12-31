var $ = require('jquery');

var StackedInlineUpdater = function($inline) {
    this.$inline = $inline;
};

StackedInlineUpdater.prototype = {
    updateObjectLinks: function() {
        var $label = this.$inline.find('.inline_label');
        var $changelink = $label.find('> .inlinechangelink');

        $label
            .find('+ a')
            .addClass('inlineviewlink')
            .text('');
        $changelink
            .text('')
            .detach()
            .insertAfter($label);
    },
    run: function() {
        try {
            this.updateObjectLinks();
        } catch (e) {
            console.error(e, e.stack);
        }

        this.$inline.addClass('initialized');
    }
};

$(document).ready(function() {
    $('.inline-related:not(.tabular)').each(function() {
        new StackedInlineUpdater($(this)).run();
    });
});
