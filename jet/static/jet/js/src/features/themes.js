require('jquery.cookie');

var $ = require('jquery');

var Themes = function() { };

Themes.prototype = {
    moveChooser: function() {
        var $chooser = $('.theme-chooser').detach();
        $('.user-tools-welcome-msg').after($chooser);
    },
    initChooser: function() {
        $('.choose-theme').on('click', function () {
            var $link = $(this);

            $.cookie('JET_THEME', $link.data('theme'), { expires: 365, path: '/' });

            var cssToLoad = [
                { url: $link.data('base-stylesheet'), class: 'base-stylesheet' },
                { url: $link.data('select2-stylesheet'), class: 'select2-stylesheet' },
                { url: $link.data('jquery-ui-stylesheet'), class: 'jquery-ui-stylesheet' }
            ];

            var loadedCss = 0;

            var onCssLoaded = function() {
                ++loadedCss;

                if (loadedCss == cssToLoad.length) {
                    $(document).trigger('theme:changed');
                }
            };

            cssToLoad.forEach(function(css) {
                $('<link>')
                    .attr('rel', 'stylesheet')
                    .addClass(css['class'])
                    .attr('href', css['url'])
                    .load(onCssLoaded)
                    .appendTo('head');
                $('.' + css['class'])
                    .slice(0, -2)
                    .remove();
            });

            $('.choose-theme').removeClass('selected');
            $link.addClass('selected');
        });
    },
    run: function() {
        try {
            this.moveChooser();
            this.initChooser();
        } catch (e) {
            console.error(e, e.stack);
        }
    }
};

$(document).ready(function() {
    new Themes().run();
});
