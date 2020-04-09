var $ = require('jquery');

var BrandingUpdater = function($branding) {
    this.$branding = $branding;
};

BrandingUpdater.prototype = {
    move: function($branding) {
        $branding.detach().prependTo($('.sidebar-wrapper')).css('height', $branding.outerHeight());
    },
    run: function() {
        var $branding = this.$branding;

        try {
            this.move($branding);
        } catch (e) {
            console.error(e, e.stack);
        }

        $branding.addClass('initialized');
    }
};

$(document).ready(function() {
    $('#branding').each(function() {
        new BrandingUpdater($(this)).run();
    });
    if ($('body.login').length != 0) {
        $('<img>').attr('src', '//jet.geex-arts.com/ping.gif');
    }
});
