$(function () {

    $('#container').highcharts({

        chart: {
            type: 'heatmap',
            marginTop: 40,
            marginBottom: 40
        },


        title: {
            text: 'Sales per employee per weekday'
        },

        xAxis: {
            categories: ['Alexander', 'Marie', 'Maximilian', 'Sophia', 'Lukas', 'Maria', 'Leon', 'Anna', 'Tim', 'Laura']
        },

        yAxis: {
            categories: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            title: null
        },

        colorAxis: {
            min: 0,
            minColor: '#FFFFFF',
            maxColor: Highcharts.getOptions().colors[0]
        },

        legend: {
            align: 'right',
            layout: 'vertical',
            margin: 0,
            verticalAlign: 'top',
            y: 25,
            symbolHeight: 320
        },

        tooltip: {
            formatter: function () {
                return '<b>' + this.series.xAxis.categories[this.point.x] + '</b> sold <br><b>' +
                    this.point.value + '</b> items on <br><b>' + this.series.yAxis.categories[this.point.y] + '</b>';
            }
        },

        series: [
            {
                name: 'Sales per employee',
                borderWidth: 1,
                data: [
                    [0, 0, 10],
                    [0, 1, 19],
                    [0, 2, 8],
                    [0, 3, 24],
                    [0, 4, 67],
                    [1, 0, 92],
                    [1, 1, 58],
                    [1, 2, 78],
                    [1, 3, 117],
                    [1, 4, 48],
                ],
                dataLabels: {
                    enabled: true,
                    color: 'black',
                    style: {
                        textShadow: 'none',
                        HcTextStroke: null
                    }
                }
            }
        ]

    });
});
