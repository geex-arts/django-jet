var $ = require('jquery');

var Filters = function($toolbar) {
    this.$toolbar = $toolbar;
};

Filters.prototype = {
    initFiltersInteraction: function($toolbar) {
        $toolbar.find('.changelist-filter-select').each(function() {
            var $select = $(this);
            var multiple = $select.attr('multiple');

            if (multiple) {
                $select.data('previous-options', $select.find('option:selected'));
            }

            $select.on('change', function() {
                var $select = $(this);
                var $selectedOption = $select.find('option:selected');

                if (multiple) {
                    if ($select.data('previous-options').length < $selectedOption.length) {
                        $selectedOption = $selectedOption.filter(function (index, option) {
                            return $select.data('previous-options').filter(function(index, initialOption) {
                                    return initialOption == option;
                                }).length == 0;
                        });
                    } else if ($select.data('previous-options').length > $selectedOption.length) {
                        $selectedOption = $select.data('previous-options').filter(function(index, initialOption) {
                            return $selectedOption.filter(function (index, option) {
                                    return initialOption == option;
                                }).length == 0;
                        });
                    }

                    $select.data('previous-options', $select.find('option:selected'));
                }

                var url = $selectedOption.data('url');
                var querysetLookup = $select.data('queryset--lookup');

                if (url) {
                    document.location = $selectedOption.data('url');
                } else if (querysetLookup) {
                    var params = {};
                    if (document.location.search) {
                        params = JSON.parse('{"' + document.location.search.substring(1).replace(/&/g, '","').replace(/=/g, '":"') + '"}',
                            function (key, value) {
                                return key === "" ? value : decodeURIComponent(value)
                            });
                    }
                    params[querysetLookup] = $selectedOption.val();
                    document.location.search = Object.keys(params).map(function (k) {
                        return encodeURIComponent(k) + '=' + encodeURIComponent(params[k])
                    }).join('&');

                }
            });
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
