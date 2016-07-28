var $ = require('jquery');

var initChangeformTabs = function() {
    $('.changeform').each(function() {
        var $changeform = $(this);
        var $tabItems = $changeform.find('.changeform-tabs-item');
        var $modules = $changeform.find('.module');

        if ($tabItems.length == 0) {
            return;
        }

        var showTab = function(selector) {
            selector = selector.replace(/^#\/?/, '');

            var $module = selector.length > 0 ? $modules.filter('#' + selector) : $();

            if ($module && $module.length == 0) {
                selector = $tabItems.first().find('a').attr('href').replace(/^#\/?/, '');
            }

            var $tabItem = $tabItems.find('a[href="#/' + selector + '"]').closest('.changeform-tabs-item');


            $tabItems.removeClass('selected');
            $tabItem.addClass('selected');
            $module = $modules.removeClass('selected').filter('#' + selector).addClass('selected');
            $module.find('select').trigger('select:init');
        };

        $('.changeform-tabs-item-link').click(function (e) {
            var moduleSelector = $(this).attr('href');

            showTab(moduleSelector);
        });

        showTab(location.hash);
    });
};

$(document).ready(function() {
    initChangeformTabs();
});
