<script>
import { HorizontalBar } from 'vue-chartjs';

export default {
  name: 'BaseChartHorizontalBar',
  extends: HorizontalBar,
  props: {
    chartdata: {
      required: true,
      type: Object,
    },
    options: {
      required: true,
      type: Object,
    },
  },
  mounted() {
    this.renderChart(this.chartdata, this.options);
  },
};
</script>