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
        var $containers = $('.action-checkbox, .action-checkbox-column, .tabular.inline-related .form-row');
        var $checkboxes = $containers
            .find('input[type="checkbox"]')
            .add('.checkbox-without-label')
            .add('label > input[type="checkbox"]');

        $checkboxes.each(function() {
            self.addLabelToCheckbox($(this));
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
