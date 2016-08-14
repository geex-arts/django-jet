/* Macedonian initialisation for the timepicker plugin */
/* Written by Stojance Panov. */
jQuery(function($){
    $.timepicker.regional['mk'] = {
                hourText: 'Час',
                minuteText: 'Минути',
                amPmText: ['Претпладне', 'Попладне'],
                closeButtonText: 'Затвори',
                nowButtonText: 'Сега',
                deselectButtonText: 'Поништи'}

    $.timepicker.setDefaults($.timepicker.regional['mk']);
});