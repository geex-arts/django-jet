var $ = require('jquery');

var Icons = function() { };

Icons.prototype = {
    updateBooleanIcons: function() {
        $('img[src$="admin/img/icon-yes.gif"]').add('img[src$="admin/img/icon-yes.svg"]').after($('<span class="icon-tick">'));
        $('img[src$="admin/img/icon-no.gif"]').add('img[src$="admin/img/icon-no.svg"]').after($('<span class="icon-cross">'));
        $('img[src$="admin/img/icon-unknown.gif"]').add('img[src$="admin/img/icon-unknown.svg"]').after($('<span class="help help-tooltip icon-question" title="' + $($('img[src$="admin/img/icon-unknown.svg"]')[0]).attr('title') + '" >'));
    },
    run: function() {
        try {
            this.updateBooleanIcons();
        } catch (e) {
            console.error(e, e.stack);
        }
    }
};

$(document).ready(function() {
    new Icons().run();
});
