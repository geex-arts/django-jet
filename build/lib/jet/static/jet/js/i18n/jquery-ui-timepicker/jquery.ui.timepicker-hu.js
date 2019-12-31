/* Hungarian initialisation for the timepicker plugin */
/* Written by Bálint Dávid Tarcsa. */
jQuery(function($){
    $.timepicker.regional['hu'] = {
                hourText: 'Óra',
                minuteText: 'Perc',
                amPmText: ['De.', 'Du.'] ,
                closeButtonText: 'Kész',
                nowButtonText: 'Most',
                deselectButtonText: 'Törlés' }
    $.timepicker.setDefaults($.timepicker.regional['hu']);
});