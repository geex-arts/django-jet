var $ = require('jquery');
var t = require('../utils/translate');

var ChangeForm = function($changeForm) {
    this.$changeForm = $changeForm;
};

ChangeForm.prototype = {
    changeDetected: false,
    onWindowBeforeUnload: function() {
        return t('Warning: you have unsaved changes');
    },
    onFormInputChanged: function($inputs) {
        $inputs.off('change', this.onFormInputChanged);

        if (!self.changeDetected) {
            $(window).bind('beforeunload', this.onWindowBeforeUnload);
        }

        this.changeDetected = true;
    },
    initUnsavedChangesWarning: function($changeForm) {
        var self = this;
        var $form = $changeForm.find('#content-main form');

        if ($form.length == 0) {
            return;
        }

        var $inputs = $form.find('input, textarea, select');

        $(document).on('submit', 'form', function() {
            $(window).off('beforeunload', self.onWindowBeforeUnload);
        });

        $inputs.on('change', $.proxy(this.onFormInputChanged, this, $inputs));
    },
    run: function() {
        try {
            this.initUnsavedChangesWarning(this.$changeForm);
        } catch (e) {
            console.error(e, e.stack);
        }
    }
};

$(document).ready(function() {
    $('.change-form').each(function() {
        new ChangeForm($(this)).run();
    });
});
