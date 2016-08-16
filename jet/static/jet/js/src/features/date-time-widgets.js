var $ = require('jquery');

require('jquery-ui/ui/core');
require('jquery-ui/ui/datepicker');

require('timepicker');

var DateTimeWidgets = function() { };

DateTimeWidgets.prototype = {
    removeInputTextNode: function($input) {
        if ($input.length == 0) {
            return;
        }

        var node = $input.get(0).previousSibling;

        if (node.nodeType == 3) {
            $(node).remove();
        }
    },
    updateDatetimeLayout: function() {
        var self = this;

        $('.form-row .datetime').each(function () {
            var $dateTime = $(this);
            var $dateField = $dateTime.find('.vDateField');
            var $timeField = $dateTime.find('.vTimeField');

            self.removeInputTextNode($dateField);
            self.removeInputTextNode($timeField);

            $dateField.nextAll('br').first().remove();
        });
    },
    djangoDateTimeFormatToJs: function(format) {
        return format.toLowerCase().replace(/%\w/g, function(format) {
            format = format.replace(/%/,"");
            return format + format;
        });
    },
    initDateWidgets: function() {
        var self = this;

        $('.form-row .vDateField').each(function () {
            var $dateField = $(this);
            var $dateButton = $('<span>').addClass('icon-calendar');
            var $dateLink = $('<a>')
                .attr('href', '#')
                .addClass('vDateField-link')
                .append($dateButton)
                .insertAfter($dateField);

            $dateField.datepicker({
                dateFormat: self.djangoDateTimeFormatToJs(DATE_FORMAT),
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
    },
    initTimeWidgets: function() {
        $('.form-row .vTimeField').each(function () {
            var $timeField = $(this);
            var $timeButton = $('<span>').addClass('icon-clock');
            var $timeLink = $('<a>')
                .attr('href', '#')
                .addClass('vTimeField-link')
                .append($timeButton)
                .insertAfter($timeField);

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
    },
    run: function() {
        try {
            this.updateDatetimeLayout();
            this.initDateWidgets();
            this.initTimeWidgets();
        } catch (e) {
            console.error(e, e.stack);
        }
    }
};

$(document).ready(function() {
    new DateTimeWidgets().run();
});
