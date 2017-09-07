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

        $('.form-row .vDateField').each(function () {
            var $dateField = $(this);
            var $dateButton = $('<span>').addClass('icon-calendar');
            $('<a>')
                .attr('href', '#')
                .addClass('vDateField-link')
                .append($dateButton)
                .insertAfter($dateField);
        });

        $('.form-row .vTimeField').each(function () {
            var $timeField = $(this);
            var $timeButton = $('<span>').addClass('icon-clock');
            $('<a>')
                .attr('href', '#')
                .addClass('vTimeField-link')
                .append($timeButton)
                .insertAfter($timeField);
        });
    },
    djangoDateTimeFormatToJs: function(format) {
        return format.toLowerCase().replace(/%\w/g, function(format) {
            format = format.replace(/%/,"");
            return format + format;
        });
    },
    initDateWidgets: function($container) {
        $container = $container || $(document);

        var self = this;

        $container.find('.form-row .vDateField').each(function () {
            var $dateField = $(this);
            var $dateLink = $dateField.next('.vDateField-link');

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
    initTimeWidgets: function($container) {
        $container = $container || $(document);

        $container.find('.form-row .vTimeField').each(function () {
            var $timeField = $(this);
            var $timeLink = $timeField.next('.vTimeField-link');

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

            var self = this;

            $('.inline-group').on('inline-group-row:added', function(e, $inlineItem) {
                $inlineItem.find('.hasDatepicker').removeClass('hasDatepicker');
                $inlineItem.find('.hasTimepicker').removeClass('hasTimepicker');
                self.initDateWidgets($inlineItem);
                self.initTimeWidgets($inlineItem);
            });
        } catch (e) {
            console.error(e, e.stack);
        }
    }
};

$(document).ready(function() {
    new DateTimeWidgets().run();
});
