var $ = window.jQuery = require('jquery');

require('jquery-ui/ui/core');
require('jquery-ui/ui/position');
require('jquery-ui/ui/widget');
require('jquery-ui/ui/tooltip');

var initTooltips = function() {
    $('a[title], .tooltip[title]').tooltip({
        track: true
    });
};

$(document).ready(function() {
    initTooltips();
});
