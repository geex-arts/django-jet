(function ($) {
    $.fn.extend( {
        googleAnalyticsChart: function() {
            var $chart = $(this);
            var ctx = $chart.get(0).getContext("2d");
            var $data = $chart.find('.chart-data');
            var $dataItems = $data.find('.chart-data-item');
            var labels = [];
            var data = [];

            $dataItems.each(function() {
                labels.push($(this).data('date'));
                data.push($(this).data('value'));
            });

            new Chart(ctx).Line({
                labels: labels,
                datasets: [
                    {
                        fillColor: $chart.find('.chart-fillColor').css('color'),
                        strokeColor: $chart.find('.chart-strokeColor').css('color'),
                        pointColor: $chart.find('.chart-pointColor').css('color'),
                        pointHighlightFill: $chart.find('.chart-pointHighlightFill').css('color'),
                        responsive: true,
                        data: data
                    }
                ]
            }, {
                scaleGridLineColor: $chart.find('.chart-scaleGridLineColor').css('color'),
                scaleLineColor: $chart.find('.chart-scaleLineColor').css('color'),
                scaleFontColor: $chart.find('.chart-scaleFontColor').css('color')
            });
        }
    });
})(jet.jQuery);