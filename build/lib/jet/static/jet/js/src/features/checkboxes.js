var $ = require('jquery');

var Checkboxes = function() { };

Checkboxes.prototype = {
    uniqueCheckboxIdCounter: 0,
    uniqueCheckboxIdPrefix: 'unique_checkbox_id_',
    addLabelToCheckbox: function($checkbox) {
        var checkboxId = $checkbox.attr('id')
            ? $checkbox.attr('id')
            : this.uniqueCheckboxIdPrefix + this.uniqueCheckboxIdCounter++;

        $checkbox.attr('id', checkboxId);
        $('<label>')
            .attr('for', checkboxId)
            .insertAfter($checkbox);
    },
    addLabelToCheckboxes: function() {
        var self = this;

        $('input[type="checkbox"]').each(function() {
            var $checkbox = $(this);

            if ($checkbox.attr('id') != undefined && $('label[for="' + $checkbox.attr('id') + '"]').length != 0) {
                return;
            }

            self.addLabelToCheckbox($checkbox);
        });
    },
    run: function() {
        try {
            this.addLabelToCheckboxes();
        } catch (e) {
            console.error(e, e.stack);
        }
    }
};

$(document).ready(function() {
    new Checkboxes().run();
});
