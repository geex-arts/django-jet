var $ = require('jquery');
var sidebar = require('../features/sidebar/main.js');

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
    initOpenSideBar: function ($breadcrumbs) {
        if (sidebar) {
            $breadcrumbs.siblings('.breadcrumbs-menu').on('click', sidebar.sideBarToggle.bind(sidebar))
        }
    },
    run: function() {
        var $breadcrumbs = this.$breadcrumbs;

        try {
            this.replaceSeparators($breadcrumbs);
            this.scrollToEnd($breadcrumbs);
            this.initOpenSideBar($breadcrumbs);
        } catch (e) {
            console.error(e, e.stack);
        }

        $breadcrumbs.addClass('initialized');
    }
};

$(document).ready(function() {
    var $breadcrumbs = $('.breadcrumbs');

    if ($breadcrumbs.length == 0) {
        $breadcrumbs = $('<div>')
            .addClass('breadcrumbs')
            .insertAfter($('#header'));
    }

    $breadcrumbs.each(function() {
        new BreadcrumbsUpdater($(this)).run();
    });
});
