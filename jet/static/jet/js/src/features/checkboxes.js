var $ = require('jquery');

var initCheckboxesWithoutLabel = function () {
    var uniqueCheckboxIdCounter = 0;
    var uniqueCheckboxIdPrefix = 'unique_checkbox_id_';

    var addLabelToCheckbox = function($checkbox) {
        var checkboxId = $checkbox.attr('id') ? $checkbox.attr('id') : uniqueCheckboxIdPrefix + uniqueCheckboxIdCounter++;
        var $label = $('<label>').attr('for', checkboxId);

        $checkbox.hide().attr('id', checkboxId);
        $label.insertAfter($checkbox);
    };

    var addLabelToCheckboxes = function() {
        var $containers = $('.action-checkbox, .action-checkbox-column').add('.tabular.inline-related .form-row');
        var $checkboxes = $containers.find('input[type="checkbox"]').add('.checkbox-without-label').add('label > input[type="checkbox"]');

        $checkboxes.each(function() {
            addLabelToCheckbox($(this));
        });
    };

    addLabelToCheckboxes();
};

$(document).ready(function() {
    initCheckboxesWithoutLabel();
});
