<template>
    <figure class="highcharts-figure">
        <div ref="chartContainer" class="chart-container"></div>
    </figure>
</template>

<script setup>
import { ref, onMounted, defineProps } from 'vue';

import Highcharts from 'highcharts';
import HighchartsMore from 'highcharts/highcharts-more';
import Stock from 'highcharts/modules/stock';
import NoDataToDisplay from 'highcharts/modules/no-data-to-display';

import { result_experiment } from '../stores/counter'
import { control_experiment } from '../stores/counter'

HighchartsMore(Highcharts);
Stock(Highcharts);
NoDataToDisplay(Highcharts);

const props = defineProps(['dataURL', 'title', 'max', 'min', 'unit', 'numDataPoints']);
const chartContainer = ref(null);
const experiment = result_experiment();
const controller = control_experiment();

const showChart = () => {
    const createChart = (container, yAxisOptions, seriesOptions) => {
        return Highcharts.chart(container, {
            chart: {
                type: 'line', // Set the chart type to 'line'
                backgroundColor: '#fafafa',
            },
            title: null,
            yAxis: {
                title: {
                    text: props.title,
                },
                min: Number(props.min), // 最小値
                max: Number(props.max), // 最大値
                // 他の yAxis オプションも設定可能
            },
            series: [{
                name: props.title,
                data: [0],
            }],
            tooltip: {
                valueSuffix: props.unit,
            },
            exporting: {
                enabled: false,
            },
        });
    };

    const targetChart = createChart(chartContainer.value, {
        title: {
            text: props.title,
        },
    });

    setInterval(async () => {
        if (controller.now_mode()) {
            if (experiment.get_result(props.title)) {
                const resultData = experiment.get_result(props.title);

                if (resultData.length < props.numDataPoints) {
                    targetChart.series[0].setData(resultData, true, true);
                } else {
                    const newData = resultData.slice(-props.numDataPoints);
                    targetChart.series[0].setData(newData, true, true);
                }
            }
        }

        else {
            targetChart.series[0].setData([0], true, true);
        }
    }, 1);
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
    - [Line chart Demo | Highcharts.com](https://www.highcharts.com/demo/highcharts/line-chart)
    - []()
 -->