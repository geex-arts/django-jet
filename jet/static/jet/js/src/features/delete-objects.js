var $ = require('jquery');

var initDeleteObjects = function() {
    $('.delete-objects-list-item.collapsable').each(function() {
        var $item = $(this);
        var $link = $item.find('.delete-objects-list-item-row-collapse');
        var $collapsable = $item.find('.delete-objects-list-item-collapsable');

        $link.on('click', function(e) {
            e.preventDefault();

            $collapsable.slideToggle(200, 'swing');
        });
    });
};

$(document).ready(function() {
    initDeleteObjects();
});
