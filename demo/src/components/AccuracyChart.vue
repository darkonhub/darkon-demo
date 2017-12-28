<script>
import { Bar, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  extends: Bar,
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
          categoryPercentage: 1.0,
          barPercentage: 0.9,
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
        display: false
      },
      tooltips: {
        enabled: true
      }
    })
  }
}
</script>
