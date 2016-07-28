var $ = require('jquery');

var initRelatedPopups = function() {
    var closeRelatedPopup = function () {
        var $popups = $('.related-popup');
        var $container = $('.related-popup-container');
        var $popup = $popups.last();

        $popup.remove();

        if ($popups.length == 1) {
            $container.fadeOut(200, 'swing', function () {
                $('.related-popup-back').hide();
                $('body').removeClass('non-scrollable');
            });
        }
    };

    $('.related-popup-back').on('click', function (e) {
        e.preventDefault();
        closeRelatedPopup();
    });

    $(window).on('related-popup:close', function () {
        closeRelatedPopup();
    });
};

$(document).ready(function() {
    initRelatedPopups();
});
