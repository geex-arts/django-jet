var $ = require('jquery');

var RelatedWidgetWrapperUpdater = function() { };

RelatedWidgetWrapperUpdater.prototype = {
    replaceLinkIcon: function(selector) {
        var $img = $(selector);

        $('<span>')
            .addClass('related-widget-wrapper-icon')
            .insertAfter($img);
        $img.remove();
    },
    updateLinkIcons: function() {
        this.replaceLinkIcon(
            'img[src*="admin/img/icon-addlink"], img[src*="admin/img/icon_addlink"]'
        );
        this.replaceLinkIcon(
            'img[src*="admin/img/icon-changelink"], img[src*="admin/img/icon_changelink"]'
        );
        this.replaceLinkIcon(
            'img[src*="admin/img/icon-deletelink"], img[src*="admin/img/icon_deletelink"]'
        );

        $('img[src*="admin/img/selector-search"]').remove();

        $('.add-related, .add-another, .change-related, .delete-related, .related-lookup')
            .addClass('initialized');
    },
    run: function() {
        try {
            this.updateLinkIcons();
        } catch (e) {
            console.error(e, e.stack);
        }
    }
};

$(document).ready(function() {
    new RelatedWidgetWrapperUpdater().run();
});
