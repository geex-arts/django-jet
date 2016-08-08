var $ = require('jquery');

var TouchMoveNonScrollable = function() { };

TouchMoveNonScrollable.prototype = {
    run: function() {
        try {
            $(document).on('touchmove', function(e) {
                var allowed = true;
                var $node = $(e.target);

                while ($node.length > 0) {
                    if ($node.hasClass('non-scrollable')) {
                        allowed = false;
                        break;
                    } else if ($node.hasClass('scrollable')) {
                        break;
                    } else {
                        $node = $node.parent();
                    }
                }

                if (!allowed) {
                    e.preventDefault();
                }
            });
        } catch (e) {
            console.error(e, e.stack);
        }
    }
};

$(document).ready(function() {
    new TouchMoveNonScrollable().run();
});
