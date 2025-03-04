<template>
  <div class="dashboard-container">
    <!-- เรียกใช้ Sidebar -->
    <Sidebar />

    <!-- ส่วนเนื้อหาหลัก -->
    <div class="content">
      <h1 class="title">พลังงานโดยรวม</h1>
      <div class="energy-circle">
        <span>70 Kwh</span>
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

.info-box {
  background: white;
  padding: 15px;
  margin: 10px 0;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
</style>
