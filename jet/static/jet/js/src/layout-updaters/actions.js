var $ = require('jquery');

var ActionsUpdater = function($changelist) {
    this.$changelist = $changelist;
};

ActionsUpdater.prototype = {
    removeLabel: function($actions) {
        var $input = $actions.find('[name="action"]').first();

        if ($input.length == 0) {
            return;
        }

        var $label = $input[0].previousSibling;

        if ($label.nodeType == 3) {
            $label.remove();
        }
    },
    moveActions: function($actions) {
        $actions.remove();
        //$actions.insertAfter(this.$changelist.find('.results'));

        var $paginator = this.$changelist.find('.paginator');
        var $wrapper = $('<div>').addClass('changelist-footer');

        $wrapper.insertAfter($paginator);

        $actions.remove();
        $paginator.remove();

        $wrapper.append($actions);
        $wrapper.append($paginator);
    },
    run: function() {
        var $actions = this.$changelist.find('.actions');

        try {
            this.removeLabel($actions);
            this.moveActions($actions);
        } catch (e) {
            console.error(e);
        }

        $actions.addClass('initialized');
    }
};

$(document).ready(function() {
    $('#changelist').each(function() {
        new ActionsUpdater($(this)).run();
    });
});
