var $ = require('jquery');

require('jquery-ui/ui/core');
require('jquery-ui/ui/position');
require('jquery-ui/ui/widget');
require('jquery-ui/ui/tooltip');
require('browsernizr/test/touchevents');
require('browsernizr');

var Tooltips = function() { };

Tooltips.prototype = {
    initTooltips: function() {
        if (!$(document.documentElement).hasClass('touchevents')) {
            $('a[title], .tooltip[title]').tooltip({
                track: true
            });
        }
    },
    run: function() {
        try {
            this.initTooltips();
        } catch (e) {
            console.error(e, e.stack);
        }
    }
};

$(document).ready(function() {
    new Tooltips($(this)).run();
});
