<template>
  <div>
    <canvas ref="barChart"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

export default {
  props: ["chartData"],
  data() {
    return {
      chart: null, // เก็บ instance ของ Chart
    };
  },
  mounted() {
    this.renderChart();
  },
  watch: {
    // ตรวจจับการเปลี่ยนแปลงของ chartData
    chartData: {
      handler() {
        if (this.chart) {
          this.chart.destroy(); // ลบกราฟเก่า
        }
        this.renderChart(); // สร้างกราฟใหม่
      },
      deep: true, // ตรวจจับการเปลี่ยนแปลงใน object อย่างลึก
    },
  },
  methods: {
    renderChart() {
      this.chart = new Chart(this.$refs.barChart, {
        type: "bar",
        data: this.chartData,
        options: {
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    },
  },
};
</script>