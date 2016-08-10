var $ = require('jquery');

var ChangeFormTabs = function($changeform) {
    this.$changeform = $changeform;
};

ChangeFormTabs.prototype = {
    getContentWrappers: function() {
        var $container = this.$changeform.find('#content-main > form > div');
        var $modules = $container.find('> .module');
        var $inlines = $container.find('> .inline-group');

        return $().add($modules).add($inlines);
    },
    getHashSelector: function(hash) {
        if (hash == undefined) {
            return null;
        }

        var result = hash.match(/^(#(\/tab\/(.+)\/)?)?$/i);

        if (result == null) {
            return null;
        }

        return result[3] != undefined ? result[3] : '';
    },
    showTab: function(hash, firstOnError) {
        var $tabItems = this.$changeform.find('.changeform-tabs-item');
        var $contentWrappers = this.getContentWrappers();
        var selector = this.getHashSelector(hash);

        if (!firstOnError && selector == null) {
            return;
        }

        if (selector == null || selector.length == 0) {
            selector = this.getHashSelector(
                $tabItems.first().find('.changeform-tabs-item-link').attr('href')
            )
        }

        var $contentWrapper = $contentWrappers.filter('.' + selector);
        var $tabItem = $tabItems
            .find('.changeform-tabs-item-link[href="#/tab/' + selector + '/"]')
            .closest('.changeform-tabs-item');

        $tabItems.removeClass('selected');
        $tabItem.addClass('selected');

        $contentWrappers.removeClass('selected');
        $contentWrapper.addClass('selected');
    },
    initTabs: function() {
        var self = this;

        $(window).on('hashchange',function() {
            self.showTab(location.hash, false);
        });

        this.showTab(location.hash, true);
    },
    updateErrorState: function() {
        var $tabItems = this.$changeform.find('.changeform-tabs-item');
        var $contentWrappers = this.getContentWrappers();
        var obj = this;

        $tabItems.each(function() {
            var $tabItem = $(this);
            var selector = obj.getHashSelector(
                $tabItem.find('.changeform-tabs-item-link').attr('href')
            );

            if (selector) {
                var $contentWrapper = $contentWrappers.filter('.' + selector);

                if ($contentWrapper.find('.form-row.errors').length) {
                    $tabItem.addClass('errors');
                }
            }
        });
    },
    run: function() {
        try {
            this.initTabs();
            this.updateErrorState();
        } catch (e) {
            console.error(e, e.stack);
        }
    }
};

$(document).ready(function() {
    $('.change-form').each(function() {
        new ChangeFormTabs($(this)).run();
    });
});
