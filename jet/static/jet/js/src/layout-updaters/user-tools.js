var $ = require('jquery');

require('browsernizr/test/touchevents');
require('browsernizr');

var UserToolsUpdater = function($usertools) {
    this.$usertools = $usertools;
};

UserToolsUpdater.prototype = {
    updateUserTools: function($usertools) {
        var $list = $('<ul>').addClass('sidebar-dependent');
        var user = $usertools.find('strong').first().text();

        $('<li>')
            .addClass('user-tools-welcome-msg')
            .text(user).appendTo($list)
            .on('click', function() {
                if ($(document.documentElement).hasClass('touchevents')) {
                    $list.toggleClass('opened');
                }
            });

        $usertools.find('a').each(function() {
            var $link = $(this);
            $('<li>').addClass('user-tools-link').html($link).appendTo($list);
        });

        $usertools.empty().addClass('user-tools').append($list);

        $list.on('mouseenter', function() {
            $list.addClass('opened');
        }).on('mouseleave', function() {
            $list.removeClass('opened');
        });
    },
    run: function() {
        try {
            this.updateUserTools(this.$usertools);
        } catch (e) {
            console.error(e, e.stack);
        }

        this.$usertools.addClass('initialized');
    }
};

$(document).ready(function() {
    $('#user-tools').each(function() {
        new UserToolsUpdater($(this)).run();
    });
});
