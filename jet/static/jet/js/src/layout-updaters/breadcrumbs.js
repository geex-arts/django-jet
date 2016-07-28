var $ = require('jquery');

var BreadcrumbsUpdater = function($breadcrumbs) {
    this.$breadcrumbs = $breadcrumbs;
};

BreadcrumbsUpdater.prototype = {
    run: function() {
        try {
            var html = this.$breadcrumbs.html();

            html = html.replace(/›/g, '<span class="icon-arrow-right breadcrumbs-separator"></span>');

            this.$breadcrumbs.html(html);
        } catch (e) {
            console.error(e);
        }

        this.$breadcrumbs.addClass('initialized');
    }
};

$(document).ready(function() {
    $('.breadcrumbs').each(function() {
        new BreadcrumbsUpdater($(this)).run();
    });
});
