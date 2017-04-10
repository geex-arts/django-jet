var $ = require('jquery');

var BreadcrumbsUpdater = function($breadcrumbs) {
    this.$breadcrumbs = $breadcrumbs;
};

BreadcrumbsUpdater.prototype = {
    replaceSeparators: function($breadcrumbs) {
        var html = $breadcrumbs.html();

        html = html.replace(/›/g, '<span class="icon-arrow-right breadcrumbs-separator"></span>');

        $breadcrumbs.html(html);
    },
    scrollToEnd: function($breadcrumbs) {
        $breadcrumbs.scrollLeft($breadcrumbs[0].scrollWidth - $breadcrumbs.width());
    },
    run: function() {
        var $breadcrumbs = this.$breadcrumbs;

        try {
            this.replaceSeparators($breadcrumbs);
            this.scrollToEnd($breadcrumbs);
        } catch (e) {
            console.error(e, e.stack);
        }

        $breadcrumbs.addClass('initialized');
    }
};

$(document).ready(function() {
    var $breadcrumbs = $('.breadcrumbs');

    if ($breadcrumbs.length == 0) {
        return;
    }

    $breadcrumbs.each(function() {
        new BreadcrumbsUpdater($(this)).run();
    });
});
