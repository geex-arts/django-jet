var $ = require('jquery');

var TabularInlineUpdater = function($inline) {
    this.$inline = $inline;
};

TabularInlineUpdater.prototype = {
    updateOriginalCell: function() {
        this.$inline.find('tr').each(function() {
            var $container = $(this).find('td.original p');

            $container.contents().each(function() {
                var $node = $(this);

                if ($node.get(0).nodeType == 3) {
                    $node.remove();
                    return;
                }

                if (!$node.hasClass('inlinechangelink')) {
                    $node.addClass('inlineviewlink');
                    return false;
                }
            });

            $container.find('a').text('');

            if ($container.children().length == 0) {
                $container.parent().addClass('empty');
            }
        });
    },
    run: function() {
        try {
            this.updateOriginalCell();
        } catch (e) {
            console.error(e, e.stack);
        }

        this.$inline.addClass('initialized');
    }
};

$(document).ready(function() {
    $('.inline-related.tabular').each(function() {
        new TabularInlineUpdater($(this)).run();
    });
});
