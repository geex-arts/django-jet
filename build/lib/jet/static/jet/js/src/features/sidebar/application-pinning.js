require('./../../utils/jquery-slidefade');

var $ = require('jquery');

require('jquery-ui/ui/core');
require('jquery-ui/ui/widget');
require('jquery-ui/ui/mouse');
require('jquery-ui/ui/draggable');
require('jquery-ui/ui/resizable');
require('jquery-ui/ui/button');
require('jquery-ui/ui/dialog');

var SideBarApplicationPinning = function($sidebar) {
    this.$sidebar = $sidebar;
};

SideBarApplicationPinning.prototype = {
    pinToggle: function($form, $sidebar, $appItem) {
        var self = this;
        var $appsList = $sidebar.find('.apps-list');
        var $pinnedAppsList = $sidebar.find('.apps-list-pinned');

        $.ajax({
            url: $form.attr('action'),
            method: $form.attr('method'),
            dataType: 'json',
            data: $form.serialize(),
            success: function (result) {
                if (result.error) {
                    return;
                }

                var $target = result.pinned ? $pinnedAppsList : $appsList;

                $appItem
                    .toggleClass('pinned', result.pinned)
                    .detach()
                    .appendTo($target);

                self.updateAppsHide($sidebar);
            }
        });
    },
    initApplicationPinning: function($sidebar) {
        var self = this;

        $sidebar.find('.pin-toggle').on('click', function(e) {
            e.preventDefault();
            e.stopPropagation();

            var $appItem = $(this).closest('.app-item');
            var appLabel = $appItem.data('app-label');
            var $form = $sidebar.find('#toggle-application-pin-form');

            $form.find('input[name="app_label"]').val(appLabel);

            self.pinToggle($form, $sidebar, $appItem);
        });

        $sidebar.find('.edit-apps-list').on('click', function(e) {
            e.preventDefault();
            $(this).parents('.sidebar-section').toggleClass('editing');
        });
    },
    updateAppsHide: function($sidebar) {
        var $appsList = $sidebar.find('.apps-list');
        var $pinnedAppsList = $sidebar.find('.apps-list-pinned');
        var $appsHide = $sidebar.find('.apps-hide');

        if (($appsList.children().length == 0 || $pinnedAppsList.children().length == 0) && $appsList.is(':visible')) {
            $appsHide.removeClass('apps-visible apps-hidden');
        } else {
            $appsHide.toggleClass('apps-visible', $appsList.is(':visible'));
            $appsHide.toggleClass('apps-hidden', !$appsList.is(':visible'));
        }
    },
    initAppsHide: function($sidebar) {
        var self = this;
        var $appsList = $sidebar.find('.apps-list');
        var $pinnedAppsList = $sidebar.find('.apps-list-pinned');
        var $appsHide = $sidebar.find('.apps-hide');

        $appsHide.on('click', function (e) {
            e.preventDefault();

            $appsList.slideFadeToggle(200, 'swing', function () {
                localStorage['side_menu_apps_list_visible'] = $appsList.is(':visible');
                self.updateAppsHide($sidebar);
            });
        });

        if (localStorage['side_menu_apps_list_visible'] === 'false') {
            if ($pinnedAppsList.children().length != 0) {
                $appsList.hide();
            } else {
                localStorage['side_menu_apps_list_visible'] = true;
            }
        }

        this.updateAppsHide($sidebar);
    },
    run: function() {
        try {
            this.initApplicationPinning(this.$sidebar);
            this.initAppsHide(this.$sidebar);
        } catch (e) {
            console.error(e, e.stack);
        }
    }
};

module.exports = SideBarApplicationPinning;
