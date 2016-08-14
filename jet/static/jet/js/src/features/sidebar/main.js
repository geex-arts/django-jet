var $ = require('jquery');
var SideBarApplicationPinning = require('./application-pinning');
var SideBarBookmarks = require('./bookmarks');
var SideBarPopup = require('./popup');

require('perfect-scrollbar/jquery')($);
require('browsernizr/test/touchevents');
require('browsernizr');

var SideBar = function($sidebar) {
    this.$sidebar = $sidebar;
};

SideBar.prototype = {
    initScrollBars: function($sidebar) {
        if (!$(document.documentElement).hasClass('touchevents')) {
            $sidebar.find('.sidebar-wrapper').perfectScrollbar();
        }
    },
    initSideBarToggle: function() {
        $('.sidebar-toggle').on('click', function(e) {
            e.preventDefault();

            var $dependent = $('.sidebar-dependent');
            var open = !$dependent.hasClass('sidebar-opened');

            $(document.body).toggleClass('non-scrollable', open);
            $dependent.toggleClass('sidebar-opened', open);
        });
    },
    run: function() {
        var $sidebar = this.$sidebar;

        new SideBarApplicationPinning($sidebar).run();
        new SideBarBookmarks($sidebar).run();
        new SideBarPopup($sidebar).run();

        try {
            this.initScrollBars($sidebar);
            this.initSideBarToggle();
        } catch (e) {
            console.error(e, e.stack);
        }

        $sidebar.addClass('initialized');
    }
};

$(document).ready(function() {
    $('.sidebar').each(function() {
        new SideBar($(this)).run();
    });
});
