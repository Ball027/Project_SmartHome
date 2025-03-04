<template>
  <div class="sidebar">
    <h2 class="user-name">ชื่อผู้ใช้</h2>
    <p class="user-role">วว/ดด/ปป</p>
    <nav class="menu">
      <ul>
        <li><router-link to="/dashboard">พลังงานโดยรวม</router-link></li>
        <li><router-link to="/room/living-room">ห้องนั่งเล่น</router-link></li>
        <li><router-link to="/room/bedroom">ห้องนอน</router-link></li>
        <li><router-link to="/room/kitchen">ห้องครัว</router-link></li>
        <li><router-link to="/room/bathroom">ห้องอาบน้ำ</router-link></li>
        <li><router-link to="/report">รายงานค่าใช้จ่าย</router-link></li>
        <li><router-link to="/notification">แจ้งเตือน</router-link></li>
      </ul>
    </nav>
    <button class="logout-btn" @click="logout">ออกระบบ</button>
  </div>
</template>

<script>
export default {
  name: "SidebarMenu",
  methods: {
    logout() {
      this.$router.push("/login");
    },
  },
};
</script>
<style>
body, html {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
}
.sidebar {
  width: 250px;
  height: 100vh;
  background-color: #0057d9; /* สีฟ้าน้ำเงิน */
  color: white;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.sidebar h2 {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
  text-align: center;
}

.sidebar p {
  font-size: 14px;
  text-align: center;
  margin-bottom: 20px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}


.sidebar ul li:hover {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 5px;
}

.menu ul {
    list-style: none;
    padding: 0;
  }
  
  .menu li {
    margin: 10px 0;
  }
  
  .menu a {
    text-decoration: none;
    color: white;
    display: block;
    padding: 8px;
    border-radius: 5px;
  }
  
  .menu a:hover {
    background-color: rgba(255, 255, 255, 0.2);
  }
  

.logout-btn {
  margin-top: auto;
  background-color: red;
  color: white;
  padding: 10px;
  text-align: center;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
}

.logout-btn:hover {
  background-color: darkred;
}
</style>
