var $ = require('jquery');

var ToolbarUpdater = function($changelist) {
    this.$changelist = $changelist;
};

ToolbarUpdater.prototype = {
    getToolbar: function($changelist) {
        var $toolbar = $changelist.find('#toolbar');

        if ($toolbar.length == 0) {
            $toolbar = $('<div>').attr('id', 'toolbar');
            $('#changelist').prepend($toolbar);
        }

        return $toolbar;
    },
    updateToolbar: function($toolbar) {
        var placeholder = $toolbar.find('input[type="submit"]').val();
        $toolbar.find('#searchbar').attr('placeholder', placeholder);
    },
    moveFilters: function($changelist, $toolbar) {
        var filterName;
        var $search = $toolbar.find('#searchbar');

        $changelist.find('#changelist-filter').children().each(function() {
            var $element = $(this);

            if ($element.prop('tagName') == 'H3') {
                filterName = $element.text();
            } else if ($element.prop('tagName') == 'UL') {
                var $select = $('<select>').addClass('changelist-filter-select');

                $element.find('li').each(function(i) {
                    var $item = $(this);
                    var $link = $item.find('a');
                    var $option = $('<option>')
                        .text($link.text())
                        .attr('data-url', $link.attr('href'))
                        .attr('selected', $item.hasClass('selected'));

                    if (i == 0 ) {
                        if (filterName != null) {
                            $option.text(filterName)
                        }

                        var $separator = $('<option>')
                            .attr('disabled', true)
                            .text('---');

                        $option = $option.add($separator);
                    }

                    $select.append($option);
                });

                var $wrapper = $('<span>')
                    .addClass('changelist-filter-select-wrapper')
                    .append($select);

                if ($search.length) {
                    $wrapper.insertAfter($search);
                } else {
                    $toolbar.append($wrapper);
                }

                filterName = null;
            }
        });

        $changelist.find('#changelist-filter').remove();
    },
    fixFloatLineBreak: function() {
        $('#content-main').each(function() {
            var $content = $(this);

            $.each(['#toolbar', '.object-tools', 'changeform-navigation'], function(i, selector) {
                var $element = $content.find(selector).first();

                if ($element.length == 0) {
                    return;
                }

                $('<div>')
                    .addClass('clear')
                    .insertAfter($element);

                return false;
            });
        });
    },
    run: function() {
        var $toolbar = this.getToolbar(this.$changelist);

        try {
            this.updateToolbar($toolbar);
            this.moveFilters(this.$changelist, $toolbar);
        } catch (e) {
            console.error(e, e.stack);
        }

        try {
            this.fixFloatLineBreak();
        } catch (e) {
            console.error(e, e.stack);
        }

        $toolbar.addClass('initialized');
    }
};

$(document).ready(function() {
    $('#changelist').each(function() {
        new ToolbarUpdater($(this)).run();
    });
});
