<template>
  <div class="dashboard-container">
    <!-- เรียกใช้ Sidebar -->
    <Sidebar />
    <!-- ส่วนเนื้อหาหลัก -->
    <div class="content">
      <!-- แสดง currentPower ของทั้ง 4 ห้อง -->
      <div class="power-grid">
        <div class="power-card">
          <span class="power-label">ห้องนั่งเล่น</span>
          <span class="power-value">{{ roomPowers.Livingroom }} W</span>
        </div>
        <div class="power-card">
          <span class="power-label">ห้องนอน</span>
          <span class="power-value">{{ roomPowers.Bedroom }} W</span>
        </div>
        <div class="power-card">
          <span class="power-label">ห้องครัว</span>
          <span class="power-value">{{ roomPowers.Kitchen }} W</span>
        </div>
        <div class="power-card">
          <span class="power-label">ห้องน้ำ</span>
          <span class="power-value">{{ roomPowers.Bathroom }} W</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from "@/components/SidebarMenu.vue";
import axios from "axios";
export default {
  name: "DashboardPage",
  components: {
    Sidebar,
  },
  data() {
    return {
      roomPowers: {
        Livingroom: 0,  // ห้องนั่งเล่น
        Bedroom: 0,     // ห้องนอน
        Kitchen: 0,     // ห้องครัว
        Bathroom: 0,    // ห้องน้ำ
      },
      userid: localStorage.getItem("userid"),
      interval: null,
    };
  },
  methods: {
    async fetchCurrentPower() {
      try {
        const response = await axios.get(`http://localhost:5000/api/current-power/${this.userid}`);
        this.roomPowers = response.data;
      } catch (error) {
        console.error("Failed to fetch current power:", error);
      }
    },
  },
  mounted() {
    this.fetchCurrentPower();
    this.interval = setInterval(() => {
      this.fetchCurrentPower();
    }, 10000);
  },
  beforeUnmount() {
    if (this.interval) {
      clearInterval(this.interval);
    }
  },
};
</script>

<style>
.dashboard-container {
  display: flex;
  width: 100vw;
  height: 100vh;
}

.content {
  flex: 1;
  padding: 20px;
  background: #f9f9f9;
}

.title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 20px;
}

.energy-circle {
  width: 150px;
  height: 150px;
  background: yellow;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 20px;
}

.power-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 2 คอลัมน์ */
  grid-template-rows: repeat(2, 1fr);    /* 2 แถว */
  gap: 20px; /* ระยะห่างระหว่างส่วน */
  width: 70%; /* ความกว้าง 70% */
  margin: 0 auto; /* จัดให้อยู่กึ่งกลาง */
  margin-bottom: 20px;
}

.power-card {
  background: white;
  padding: 20px; /* เพิ่ม padding เพื่อให้ขนาดใหญ่ขึ้น */
  border-radius: 10px; /* ปรับขอบมน */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* เพิ่มเงา */
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.power-label {
  font-size: 1.2rem; /* ปรับขนาดตัวอักษร */
  font-weight: bold;
  margin-bottom: 10px; /* เพิ่มระยะห่าง */
}

.power-value {
  font-size: 1.5rem; /* ปรับขนาดตัวอักษร */
  color: #333;
}
</style>