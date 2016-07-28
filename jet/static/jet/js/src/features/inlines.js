var $ = require('jquery');

var initInlines = function() {
    $('.module').each(function() {
        var $module = $(this);
        var $items = function() { return $module.find('.stacked-inline-list-item'); };
        var $inlinesRelated = function() { return $module.find('.inline-related'); };

        $module.on('click', '.stacked-inline-list-item-link', function(e) {
            var $itemLink = $(this);
            var $item = $itemLink.closest('.stacked-inline-list-item');
            var moduleId = $itemLink.data('inline-related-id');

            $items().removeClass('selected');
            $item.addClass('selected');
            $inlinesRelated().removeClass('selected').filter('#' + moduleId).addClass('selected');

            e.preventDefault();
        });

        $module.on('click', '.stacked-inline-list-item-link-remove', function(e) {
            var $itemLink = $(this).closest('.stacked-inline-list-item-link');
            var $item = $itemLink.closest('.stacked-inline-list-item');
            var moduleId = $itemLink.data('inline-related-id');

            $item.remove();
            $inlinesRelated().filter('#' + moduleId).remove();

            e.preventDefault();
        });

        $module.find('.inline-related').each(function() {
            var $inline = $(this);

            $inline.find('.delete input').on('change', function(e) {
                var $input = $(this);
                var id = $inline.attr('id');
                var $link = $module.find('.stacked-inline-list-item-link[data-inline-related-id="' + id + '"]');
                var $item = $link.closest('.stacked-inline-list-item');

                if ($input.is(':checked')) {
                    $item.addClass('delete');
                } else {
                    $item.removeClass('delete');
                }
            });
        });

        $module.find('.add-row a').on('click', function() {
           $module.find('select').trigger('select:init');
        });
    });
};

$(document).ready(function() {
    initInlines();
});
