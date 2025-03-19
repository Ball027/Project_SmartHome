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
          <span class="power-value">{{ currentPower.livingRoom }} W</span>
        </div>
        <div class="power-card">
          <span class="power-label">ห้องนอน</span>
          <span class="power-value">{{ currentPower.bedroom }} W</span>
        </div>
        <div class="power-card">
          <span class="power-label">ห้องครัว</span>
          <span class="power-value">{{ currentPower.kitchen }} W</span>
        </div>
        <div class="power-card">
          <span class="power-label">ห้องน้ำ</span>
          <span class="power-value">{{ currentPower.bathroom }} W</span>
        </div>
      </div>

      <div class="info-box">
        <h3>5 ทริคการประหยัดพลังงาน!!</h3>
      </div>
      <div class="info-box">
        <h3>โซลาร์เซลล์คุ้มค่าจริงหรือไม่?</h3>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from "@/components/SidebarMenu.vue";

export default {
  name: "DashboardPage",
  components: {
    Sidebar,
  },
  data() {
    return {
      currentPower: {
        livingRoom: 20, // พลังงานห้องนั่งเล่น (หน่วย: W)
        bedroom: 15,    // พลังงานห้องนอน (หน่วย: W)
        kitchen: 10,    // พลังงานห้องครัว (หน่วย: W)
        bathroom: 5,    // พลังงานห้องน้ำ (หน่วย: W)
      },
    };
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
  grid-template-columns: repeat(4, 1fr); /* 4 ส่วนใน 1 แถว */
  gap: 10px; /* ระยะห่างระหว่างส่วน */
  margin-bottom: 20px;
}

.power-card {
  background: white;
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.power-label {
  font-size: 1rem;
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

.power-value {
  font-size: 1.1rem;
  color: #333;
}

.info-box {
  background: white;
  padding: 15px;
  margin: 10px 0;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
</style>