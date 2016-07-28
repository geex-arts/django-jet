var $ = require('jquery');

var initFilters = function() {
    $('.changelist-filter-select').on('change', function () {
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
};

$(document).ready(function() {
    initFilters();
});
