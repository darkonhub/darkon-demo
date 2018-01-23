<script>
import { Line, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  extends: Line,
  mixins: [reactiveProp],
  mounted () {
    // Overwriting base render method with actual data.
    this.renderChart(this.chartData, {
      responsive: true,
      maintainAspectRatio: true,
      scales: {
        scaleLabel: {
          display: false
        },
        xAxes: [{
          gridLines: {
            display: true
          }
        }],
        yAxes: [{
          gridLines: {
            display: true
          }
        }]
      },
      legend: {
        display: true
      },
      tooltips: {
        enabled: true
      }
    })
  }
}
</script>
