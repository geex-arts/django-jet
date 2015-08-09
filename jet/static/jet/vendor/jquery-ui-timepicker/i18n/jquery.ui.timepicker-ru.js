/* Russian initialisation for the timepicker plugin */
/* Written by Denis Kildishev. */
jQuery(function($){
    $.timepicker.regional['ru'] = {
                hourText: 'Час',
                minuteText: 'Минута',
                amPmText: ['AM', 'PM'] ,
                closeButtonText: 'Закрыть',
                nowButtonText: 'Сейчас',
                deselectButtonText: 'Очистить' }
    $.timepicker.setDefaults($.timepicker.regional['ru']);
});
