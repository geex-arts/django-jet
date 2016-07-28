var $ = require('jquery');

var initUnsavedChangesWarning = function() {
    var $changeform = $('.change-form #content-main form');

    if ($changeform.length) {
        var $inputs = $changeform.find('input, textarea, select');
        var bound = false;

        var onBeforeUnload = function() {
            return django.gettext('Warning: you have unsaved changes');
        };

        var onChange = function() {
            $inputs.off('change', onChange);

            if (!bound) {
                $(window).bind('beforeunload', onBeforeUnload);

                bound = true;
            }
        };

        $(document).on('submit', 'form', function() {
            $(window).off('beforeunload', onBeforeUnload);
        });

        $inputs.on('change', onChange);
    }
};

$(document).ready(function() {
    initUnsavedChangesWarning();
});
