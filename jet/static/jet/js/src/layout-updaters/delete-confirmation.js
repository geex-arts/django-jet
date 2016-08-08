var $ = require('jquery');

var DeleteConfirmationUpdater = function() { };

DeleteConfirmationUpdater.prototype = {
    run: function() {
        try {
            if ($('.delete-confirmation-marker').length != 0) {
                $('body').addClass('delete-confirmation');
            }
        } catch (e) {
            console.error(e, e.stack);
        }
    }
};

$(document).ready(function() {
    new DeleteConfirmationUpdater().run();
});
