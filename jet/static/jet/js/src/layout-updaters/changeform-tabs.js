var $ = require('jquery');
var t = require('../utils/translate');

var ChangeFormTabsUpdater = function($changeform) {
    this.$changeform = $changeform;
};

ChangeFormTabsUpdater.prototype = {
    findTabs: function($modules, $inlines) {
        var tabs = [];

        $modules.each(function(i) {
            var $module = $(this);
            var $header = $module.find('> h2').first();
            var title = $header.length != 0 ? $header.html() : t('General');
            var className = 'module_' + i;

            $module.addClass(className);
            $header.remove();

            tabs.push({
                className: className,
                title: title
            });
        });

        $inlines.each(function(i) {
            var $inline = $(this);
            var $header = $inline.find('> h2, > fieldset.module > h2, .tabular.inline-related > .module > h2').first();
            var title = $header.length != 0 ? $header.html() : t('General');
            var className = 'inline_' + i;

            $inline.addClass(className);
            $header.remove();

            tabs.push({
                className: className,
                title: title
            });
        });

        return tabs;
    },
    createTabs: function($contentWrappers, tabs) {
        if (tabs.length < 2) {
            return;
        }

        var $tabs = $('<ul>').addClass('changeform-tabs');

        $.each(tabs, function() {
            var tab = this;
            var $item = $('<li>')
                .addClass('changeform-tabs-item');
            var $link = $('<a>')
                .addClass('changeform-tabs-item-link')
                .html(tab.title)
                .attr('href', '#/tab/' + tab.className + '/');

            $link.appendTo($item);
            $item.appendTo($tabs);
        });

        $tabs.insertBefore($contentWrappers.first());
    },
    run: function() {
        var $container = this.$changeform.find('#content-main > form > div');
        var $modules = $container.find('> .module');
        var $inlines = $container.find('> .inline-group');
        var $contentWrappers = $().add($modules).add($inlines);

        try {
            var tabs = this.findTabs($modules, $inlines);
            this.createTabs($contentWrappers, tabs);
        } catch (e) {
            console.error(e, e.stack);
        }

        $contentWrappers.addClass('initialized');
    }
};

$(document).ready(function() {
    $('.change-form').each(function() {
        new ChangeFormTabsUpdater($(this)).run();
    });
});
