var $ = require('jquery');

var Siblings = function($siblings) {
    this.$siblings = $siblings;
};

Siblings.prototype = {
    moveSiblings: function($siblings) {
        $siblings.remove().insertBefore($('.object-tools'));
    },
    run: function() {
        try {
            this.moveSiblings(this.$siblings);
        } catch (e) {
            console.error(e);
        }

        this.$siblings.addClass('initialized');
    }
};

$(document).ready(function() {
    $('.changeform-navigation').each(function() {
        new Siblings($(this)).run();
    });
});
