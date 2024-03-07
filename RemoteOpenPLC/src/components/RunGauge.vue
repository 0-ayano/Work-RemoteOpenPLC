<template>
    <figure class="highcharts-figure">
        <div ref="chartContainer" class="chart-container"></div>
    </figure>
</template>
  
<script setup>
import { ref, onMounted, defineProps } from 'vue';

import axios from 'axios';
import Highcharts from 'highcharts';
import HighchartsMore from 'highcharts/highcharts-more';
import Stock from 'highcharts/modules/stock';
import NoDataToDisplay from 'highcharts/modules/no-data-to-display';
import SolidGauge from 'highcharts/modules/solid-gauge';

import { result_experiment } from '../stores/counter'
import { control_experiment } from '../stores/counter'

HighchartsMore(Highcharts);
Stock(Highcharts);
NoDataToDisplay(Highcharts);
SolidGauge(Highcharts);

const props = defineProps(['dataURL', 'title', 'max', 'min', 'unit']);
const chartContainer = ref(null);
const experiment = result_experiment()
const controller = control_experiment();

const showChart = () => {
    const createChart = (container, yAxisOptions, seriesOptions) => {
        return Highcharts.chart(container, Highcharts.merge(gaugeOptions, {
            yAxis: yAxisOptions,
            series: [seriesOptions],
        }));
    };

    const gaugeOptions = {
        chart: {
            type: 'solidgauge',
            backgroundColor: '#fafafa',
        },
        title: null,
        pane: {
            center: ['50%', '85%'],
            size: '140%',
            startAngle: -90,
            endAngle: 90,
            background: {
                backgroundColor: Highcharts.defaultOptions.legend.backgroundColor || '#EEE',
                innerRadius: '60%',
                outerRadius: '100%',
                shape: 'arc',
            },
        },
        exporting: {
            enabled: false,
        },
        tooltip: {
            enabled: false,
        },
        yAxis: {
            lineWidth: 0,
            tickWidth: 0,
            minorTickInterval: null,
            tickAmount: 2,
            title: {
                y: -70,
            },
            labels: {
                y: 16,
            },
        },
        plotOptions: {
            solidgauge: {
                dataLabels: {
                    y: 5,
                    borderWidth: 0,
                    useHTML: true,
                },
            },
        },
    };

    const targetChart = createChart(chartContainer.value, {
        min: Number(props.min),
        max: Number(props.max),
        title: {
            text: props.title,
        },
    }, {
        name: props.title,
        data: [experiment.get_new_result(props.title)],
        dataLabels: {
            format: '<div style="text-align:center">' +
                '<span style="font-size:25px">{y:.1f}</span><br/>' +
                '<span style="font-size:12px;opacity:0.4">' +
                props.unit +
                '</span>' +
                '</div>',
        },
        tooltip: {
            valueSuffix: props.unit,
        },
    });

    setInterval(async () => {
        if (controller.now_mode()) {
            try {
                const res = await axios.get("http://127.0.0.1:8000/register/" + props.dataURL);
                experiment.push_result(props.title, Number(res.data))
                targetChart.series[0].setData([Number(res.data)], true);

            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }

        else {
            experiment.clear_result()
            targetChart.series[0].setData([0], true, true);
        }
    }, 1500);
};

onMounted(() => {
    if (chartContainer.value) {
        showChart();
    }
});



</script>

<style scoped>
.highcharts-figure .chart-container {
    width: 300px;
    height: 200px;
}

.highcharts-data-table table {
    font-family: Verdana, sans-serif;
    border-collapse: collapse;
    border: 1px solid #ebebeb;
    margin: 10px auto;
    text-align: center;
    width: 100%;
    max-width: 500px;
}

.highcharts-data-table caption {
    padding: 1em 0;
    font-size: 1.2em;
    color: #555;
}

.highcharts-data-table th {
    font-weight: 600;
    padding: 0.5em;
}

.highcharts-data-table td,
.highcharts-data-table th,
.highcharts-data-table caption {
    padding: 0.5em;
}

.highcharts-data-table thead tr,
.highcharts-data-table tr:nth-child(even) {
    background: #f8f8f8;
}

.highcharts-data-table tr:hover {
    background: #f1f7ff;
}
</style>

<!-- 
	Reference
    - [Error while loading solid gauge module](https://www.highcharts.com/forum/viewtopic.php?t=48659)
    - [Highcharts Vue Solid Gauge - CodeSandbox](https://codesandbox.io/p/sandbox/highcharts-vue-solid-gauge-oyeppq?file=%2Fsrc%2Fmain.js%3A18%2C1)
    - [Solid gauge Demo | Highcharts.com](https://www.highcharts.com/demo/highcharts/gauge-solid)
    - []()
 -->