var $ = window.jQuery = require('jquery');

require('jquery-ui/ui/core');
require('jquery-ui/ui/datepicker');

require('timepicker');

var initDateTimeWidgets = function() {
    var removePreviousSibling = function($element) {
        var node = $element[0].previousSibling;
        node.parentNode.removeChild(node);
    };

    var djangoDateTimeFormatToJs = function(format) {
        return format.toLowerCase().replace(/%\w/g, function(format) {
            format = format.replace(/%/,"");
            return format + format;
        });
    };

    var updateDatetimeLayout = function() {
        $('.form-row .datetime').each(function () {
            var $dateTime = $(this);
            var $dateField = $dateTime.find('.vDateField');
            var $timeField = $dateTime.find('.vTimeField');

            removePreviousSibling($dateField);
            removePreviousSibling($timeField);

            $dateField.nextAll('br').first().remove();
        });
    };

    var initDateWidget = function() {
        $('.form-row .vDateField').each(function () {
            var $dateField = $(this);
            var $dateLink = $('<a href="#">').addClass('vDateField-link');
            var $dateButton = $('<span>').addClass('icon-calendar');

            $dateLink.append($dateButton).insertAfter($dateField);

            $dateField.datepicker({
                dateFormat: djangoDateTimeFormatToJs(DATE_FORMAT),
                showButtonPanel: true,
                nextText: '',
                prevText: ''
            });
            $dateLink.on('click', function (e) {
                if ($dateField.datepicker('widget').is(':visible')) {
                    $dateField.datepicker('hide');
                } else {
                    $dateField.datepicker('show');
                }

                e.preventDefault();
            });
        });

        var old_goToToday = $.datepicker._gotoToday;
        $.datepicker._gotoToday = function(id) {
            old_goToToday.call(this,id);
            this._selectDate(id);
        };
    };

    var initTimeWidget = function() {
        $('.form-row .vTimeField').each(function () {
            var $timeField = $(this);
            var $timeLink = $('<a href="#">').addClass('vTimeField-link');
            var $timeButton = $('<span>').addClass('icon-clock');

            $timeLink.append($timeButton).insertAfter($timeField);

            $timeField.timepicker({
                showPeriodLabels: false,
                showCloseButton: true,
                showNowButton: true
            });
            $timeLink.on('click', function (e) {
                if ($timeField.datepicker('widget').is(':visible')) {
                    $timeField.datepicker('hide');
                } else {
                    $timeField.timepicker('show');
                }

                e.preventDefault();
            });
        });
    };

    updateDatetimeLayout();
    initDateWidget();
    initTimeWidget();
};

$(document).ready(function() {
    initDateTimeWidgets();
});
