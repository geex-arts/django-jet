var $ = require('jquery');

var Filters = function($toolbar) {
    this.$toolbar = $toolbar;
};

var parseQueryStringToDictionary = function(queryString) {
	var dictionary = {};

	if (queryString.indexOf('?') === 0) {
		queryString = queryString.substr(1);
	}

	var parts = queryString.split('&');

	for(var i = 0; i < parts.length; i++) {
	    if (parts[i].length === 0) {
	        continue
        }
		var p = parts[i];
		var keyValuePair = p.split('=');

		var key = keyValuePair[0];
		var value = keyValuePair[1];
		value = decodeURIComponent(value);
		value = value.replace(/\+/g, ' ');

		dictionary[key] = value;
	}

	return dictionary;
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
                    var params = parseQueryStringToDictionary(document.location.search);
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
