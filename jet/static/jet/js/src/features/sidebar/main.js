var $ = window.jQuery = require('jquery');
var SideBarApplicationPinning = require('./application-pinning');
var SideBarBookmarks = require('./bookmarks');
var SideBarPopup = require('./popup');

require('perfect-scrollbar/jquery')($);

var SideBar = function($sidebar) {
    this.$sidebar = $sidebar;
};

SideBar.prototype = {
    initScrollBars: function($sidebar) {
        $sidebar.find('.sidebar-wrapper').perfectScrollbar();
    },
    run: function() {
        var $sidebar = this.$sidebar;

        new SideBarApplicationPinning($sidebar).run();
        new SideBarBookmarks($sidebar).run();
        new SideBarPopup($sidebar).run();

        try {
            this.initScrollBars($sidebar);
        } catch (e) {
            console.error(e);
        }

        $sidebar.addClass('initialized');
    }
};

$(document).ready(function() {
    $('.sidebar').each(function() {
        new SideBar($(this)).run();
    });
});
