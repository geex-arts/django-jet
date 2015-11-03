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

            var chart = new Chart(ctx).Line({
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

            var updateChartColors = function(chart) {
                for (var i = 0; i < chart.datasets.length; ++i) {
                    chart.datasets[i]['fillColor'] = $chart.find('.chart-fillColor').css('color');
                    chart.datasets[i]['strokeColor'] = $chart.find('.chart-strokeColor').css('color');
                    chart.datasets[i]['pointColor'] = $chart.find('.chart-pointColor').css('color');
                    chart.datasets[i]['pointHighlightFill'] = $chart.find('.chart-pointHighlightFill').css('color');
                }

                chart.scale['gridLineColor'] = $chart.find('.chart-scaleGridLineColor').css('color');
                chart.scale['lineColor'] = $chart.find('.chart-scaleLineColor').css('color');
                chart.scale['textColor'] = $chart.find('.chart-scaleFontColor').css('color');

                chart.update();
            };

            $(document).on('theme:changed', function() {
                updateChartColors(chart);
            });
        }
    });
})(jet.jQuery);