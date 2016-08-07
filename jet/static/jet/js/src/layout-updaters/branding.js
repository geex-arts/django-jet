var $ = require('jquery');

var BrandingUpdater = function($branding) {
    this.$branding = $branding;
};

BrandingUpdater.prototype = {
    run: function() {
        var $branding = this.$branding;

        try {
            $branding.detach().prependTo($('.sidebar-wrapper'));
        } catch (e) {
            console.error(e);
        }

        $branding.addClass('initialized');
    }
};

$(document).ready(function() {
    $('#branding').each(function() {
        new BrandingUpdater($(this)).run();
    });
});
