<template>
  <div class="layout">
    <Sidebar />
    <div class="report-container">
      <h2 class="report-title">รายงานค่าใช้จ่ายที่เกิดขึ้น</h2>

      <!-- Dropdown เลือกปี -->
      <div class="filter-container">
        <label for="year">ปี</label>
        <select id="year" v-model="selectedYear" @change="fetchReportData">
          <option v-for="year in years" :key="year" :value="year">
            {{ year }}
          </option>
        </select>
      </div>

      <!-- กราฟแท่ง -->
      <div class="chart-container">
        <BarChart :chart-data="chartData" />
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from "@/components/SidebarMenu.vue";
import BarChart from "@/components/BarChart.vue"; // Import component กราฟ
import axios from "axios"; // ใช้ Axios ดึงข้อมูลจาก API

export default {
  name: "ReportPage",
  components: {
    Sidebar,
    BarChart,
  },
  data() {
    return {
      selectedYear: new Date().getFullYear(), // เริ่มต้นด้วยปีปัจจุบัน
      years: [], // ปีที่มีข้อมูลในฐานข้อมูล
      chartData: {
        labels: [
          "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
          "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
        ], // ชื่อเดือน
        datasets: [
          {
            label: "พลังงานทั้งหมด (kWh)",
            backgroundColor: "green",
            data: [], // พลังงานทั้งหมดในแต่ละเดือน
          },
          {
            label: "ค่าใช้จ่าย (บาท)",
            backgroundColor: "blue",
            data: [], // ค่าใช้จ่ายในแต่ละเดือน
          },
        ],
      },
    };
  },
  async created() {
    await this.fetchYears(); // ดึงปีที่มีข้อมูล
    await this.fetchReportData(); // ดึงข้อมูลรายงาน
  },
  methods: {
    // ดึงปีที่มีข้อมูลในฐานข้อมูล
    async fetchYears() {
      try {
        const response = await axios.get("/api/reports/years");
        this.years = response.data;
      } catch (error) {
        console.error("Failed to fetch years:", error);
      }
    },
    // ดึงข้อมูลรายงาน
    async fetchReportData() {
      try {
        const response = await axios.get(`/api/reports?year=${this.selectedYear}`);
        const reports = response.data;

        // เตรียมข้อมูลสำหรับกราฟ
        const energyData = Array(12).fill(0); // พลังงานทั้งหมดในแต่ละเดือน
        const costData = Array(12).fill(0); // ค่าใช้จ่ายในแต่ละเดือน

        reports.forEach(report => {
          const month = parseInt(report["month/year"].split("-")[1]) - 1; // แปลงเดือนเป็น index (0-11)
          energyData[month] = report.total_energy;
          costData[month] = report.total_cost;
        });

        // อัปเดตข้อมูลกราฟ
        this.chartData.datasets[0].data = energyData;
        this.chartData.datasets[1].data = costData;
      } catch (error) {
        console.error("Failed to fetch report data:", error);
      }
    },
  },
};
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
}

.report-container {
  flex-grow: 1;
  padding: 20px;
  overflow: auto;
}

.report-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.chart-container {
  background: #ddd;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.filter-container {
  margin-bottom: 20px;
}
</style>