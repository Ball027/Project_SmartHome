<template>
    <div class="layout">
      <Sidebar />
      <div class="notification-container">
        <h2 class="notification-title">การแจ้งเตือน</h2>
        <div class="notification-list">
          <div
            v-for="(notification, index) in notifications"
            :key="index"
            class="notification-item"
          >
            <span class="device-name">ชื่ออุปกรณ์</span>
            <span class="alert-text">พบการใช้งานที่ผิดปกติ</span>
            <span
              class="power-usage"
              :class="{ 'high-power': notification.power > 100, 'low-power': notification.power <= 100 }"
            >
              {{ notification.power }} Kw
            </span>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Sidebar from "@/components/SidebarMenu.vue";
  
  export default {
    name: "NotificationPage",
    components: {
      Sidebar,
    },
    data() {
      return {
        notifications: [{ power: 200 }, { power: 20 }],
      };
    },
  };
  </script>
  
  <style scoped>
  /* ให้ Sidebar และเนื้อหาอยู่ข้างกัน */
  .layout {
    display: flex;
    height: 100vh;
  }
  
  /* Sidebar มีขนาดคงที่ */
  .layout Sidebar {
    width: 250px;
    flex-shrink: 0;
  }
  
  /* ทำให้เนื้อหาแจ้งเตือนขยายเต็มที่ */
  .notification-container {
    flex-grow: 1;
    padding: 20px;
  }
  
  /* รูปแบบรายการแจ้งเตือน */
  .notification-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 10px;
  }
  
  .notification-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .notification-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #f0f0f0;
    padding: 10px;
    border-radius: 5px;
  }
  
  .device-name {
    font-weight: bold;
  }
  
  .alert-text {
    margin-left: 10px;
    color: black;
  }
  
  .power-usage {
    font-weight: bold;
  }
  
  .high-power {
    color: red;
  }
  
  .low-power {
    color: orange;
  }
  </style>
  