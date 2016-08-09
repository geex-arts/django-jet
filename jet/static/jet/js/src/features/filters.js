var $ = require('jquery');

var Filters = function($toolbar) {
    this.$toolbar = $toolbar;
};

Filters.prototype = {
    initFiltersInteraction: function($toolbar) {
        $toolbar.find('.changelist-filter-select').on('change', function () {
            var $select = $(this);
            var $selectedOption = $select.find('option:selected');
            var url = $selectedOption.data('url');
            var querysetLookup = $select.data('queryset--lookup');

            if (url) {
                document.location = $selectedOption.data('url');
            } else if (querysetLookup) {
                document.location = '?' + querysetLookup + '=' + $selectedOption.val();
            }
        });
    },
    run: function() {
        try {
            this.initFiltersInteraction(this.$toolbar);
        } catch (e) {
            console.error(e, e.stack);
        }
    }
};

$(document).ready(function() {
    $('#toolbar').each(function() {
        new Filters($(this)).run();
    });
});
