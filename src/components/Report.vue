<template>
  <div class="layout">
    <Sidebar />
    <div class="report-container">
      <h2 class="report-title">รายงานค่าใช้จ่ายที่เกิดขึ้น</h2>

      <!-- Dropdown เลือกปี -->
      <div class="filter-container">
        <label for="year">ระบุปีที่ต้องการ</label>
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
      <div class="filter-container">
        <label for="month">ระบุเดือนที่ต้องการ</label>
        <select id="month" v-model="selectedMonth" @change="fetchReportData">
          <option v-for="(month, index) in months" :key="index" :value="index + 1">
            {{ month }}
          </option>
        </select>
      </div>
      <div class="room-energy-grid">
        <div class="room-energy-card" v-for="(energy, room) in currentRoomEnergies" :key="room">
          <span class="room-name">{{ room }}</span>
          <span class="room-energy">{{ energy }} Wh</span>
        </div>
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
      selectedMonth: new Date().getMonth() + 1, // เริ่มต้นด้วยเดือนปัจจุบัน
      years: [], // ปีที่มีข้อมูลในฐานข้อมูล
      months: [
        "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
        "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
      ],
      noData: false, // ตรวจสอบว่ามีข้อมูลหรือไม่
      livingroom_energy: Array(12).fill(0),
      bedroom_energy: Array(12).fill(0),
      kitchen_energy: Array(12).fill(0),
      bathroom_energy: Array(12).fill(0),
      chartData: {
        labels: [
          "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
          "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
        ], // ชื่อเดือน
        datasets: [
          {
            label: "พลังงานทั้งหมด (Wh)",
            backgroundColor: "green",
            data: [], // พลังงานทั้งหมดในแต่ละเดือน
          },
          {
            label: "ค่าใช้จ่าย (บาท)",
            backgroundColor: "red",
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
        const response = await axios.get("http://localhost:5000/api/reports/years");
        this.years = response.data;
        if (this.years.length > 0) {
          this.selectedYear = this.years[0]; // เลือกปีแรกเป็นค่าเริ่มต้น
        }
      } catch (error) {
        console.error("Failed to fetch years:", error);
      }
    },
    // ดึงข้อมูลรายงาน
    async fetchReportData() {
      try {
        const response = await axios.get(`http://localhost:5000/api/reports?year=${this.selectedYear}`);
        const reports = response.data;

        if (reports.length === 0) {
          this.noData = true; // ไม่มีข้อมูล
          return;
        }

        // เตรียมข้อมูลสำหรับกราฟ
        const energyData = Array(12).fill(0); // พลังงานทั้งหมดในแต่ละเดือน
        const costData = Array(12).fill(0); // ค่าใช้จ่ายในแต่ละเดือน
        this.livingroom_energy = Array(12).fill(0);
        this.bedroom_energy = Array(12).fill(0);
        this.kitchen_energy = Array(12).fill(0);
        this.bathroom_energy = Array(12).fill(0);

        reports.forEach(report => {
          const month = parseInt(report["month/year"].split("-")[1]) - 1; // แปลงเดือนเป็น index (0-11)
          energyData[month] = report.total_energy || 0;
          costData[month] = report.total_cost || 0;
          this.livingroom_energy[month] = report.livingroom_energy || 0;
          this.bedroom_energy[month] = report.bedroom_energy || 0;
          this.kitchen_energy[month] = report.kitchen_energy || 0;
          this.bathroom_energy[month] = report.bathroom_energy || 0;
        });

        // อัปเดตข้อมูลกราฟ
        this.chartData.datasets[0].data = energyData;
        this.chartData.datasets[1].data = costData;
        // console.log("พลังงาน",this.chartData.datasets[0].data);
        // console.log("ค่าใช้จ่าย", this.chartData.datasets[1].data);
        // console.log("livingroom_energy", this.livingroom_energy);
      } catch (error) {
        console.error("Failed to fetch report data:", error);
      }
    },
  },
  computed: {
    // คำนวณพลังงานของแต่ละห้องตามเดือนที่เลือก
    currentRoomEnergies() {
      const monthIndex = this.selectedMonth - 1;
      return {
        "ห้องนั่งเล่น": this.livingroom_energy[monthIndex] || 0,
        "ห้องนอน": this.bedroom_energy[monthIndex] || 0,
        "ห้องครัว": this.kitchen_energy[monthIndex] || 0,
        "ห้องอาบน้ำ": this.bathroom_energy[monthIndex] || 0,
      };
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

.no-data-message {
  color: red;
  font-size: 1.2rem;
  text-align: center;
  margin-top: 20px;
}

.room-energy-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-top: 20px;
}

.room-energy-card {
  background: #f0f0f0;
  padding: 15px;
  border-radius: 10px;
  text-align: center;
}

.room-name {
  font-size: 1.2rem;
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

.room-energy {
  font-size: 1.1rem;
  color: #333;
}
</style>