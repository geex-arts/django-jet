var $ = require('jquery');

var ScrollToBottomDetector = function() { };

ScrollToBottomDetector.prototype = {
    prevScrollTop: null,
    initDetector: function() {
        var self = this;

        $(window).on('scroll', function() {
            if (self.prevScrollTop != null && $(window).scrollTop() > self.prevScrollTop && $(window).scrollTop() > 60) {
                $(document.body).addClass('scroll-to-bottom');
            } else {
                $(document.body).removeClass('scroll-to-bottom');
            }

            self.prevScrollTop = $(window).scrollTop();
        });
    },
    run: function() {
        try {
            this.initDetector();
        } catch (e) {
            console.error(e, e.stack);
        }
    }
};

$(document).ready(function() {
    new ScrollToBottomDetector().run();
});
