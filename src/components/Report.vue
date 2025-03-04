<template>
    <div class="layout">
      <Sidebar />
      <div class="report-container">
        <h2 class="report-title">รายงานค่าใช้จ่ายที่เกิดขึ้น</h2>
  
        <!-- กราฟแท่ง -->
        <div class="chart-container">
          <BarChart :chart-data="chartData" />
        </div>
  
        <!-- Dropdown เลือกเดือน -->
        <div class="filter-container">
          <label for="month">เดือน</label>
          <select id="month" v-model="selectedMonth">
            <option v-for="month in months" :key="month" :value="month">
              {{ month }}
            </option>
          </select>
        </div>
  
        <!-- แสดงข้อมูลพลังงานของแต่ละห้อง -->
        <div class="room-usage-grid">
          <div class="room-usage-card" v-for="(usage, room) in roomUsages" :key="room">
            <span class="room-name">{{ room }}</span>
            <span class="room-energy">{{ usage }} Kwh</span>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Sidebar from "@/components/SidebarMenu.vue";
  import BarChart from "@/components/BarChart.vue"; // Import component กราฟ
  
  export default {
    name: "ReportPage",
    components: {
      Sidebar,
      BarChart,
    },
    data() {
      return {
        selectedMonth: "มกราคม 2567",
        months: ["มกราคม 2567", "กุมภาพันธ์ 2567", "มีนาคม 2567", "เมษายน 2567"],
        roomUsages: {
          "ห้องนั่งเล่น": 50,
          "ห้องนอน": 50,
          "ห้องครัว": 50,
          "ห้องอาบน้ำ": 50,
        },
        chartData: {
          labels: ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย."],
          datasets: [
            {
              label: "ค่าใช้จ่าย (บาท)",
              backgroundColor: "green",
              data: [1200, 900, 1100, 500], // ค่าใช้จ่ายแต่ละเดือน
            },
          ],
        },
      };
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
  
  .room-usage-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
  
  .room-usage-card {
    background: #f0f0f0;
    padding: 10px;
    border-radius: 5px;
    display: flex;
    justify-content: space-between;
  }
  </style>
  