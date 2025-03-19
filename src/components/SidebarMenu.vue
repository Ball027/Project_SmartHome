<template>
  <div class="sidebar">
    <h2 class="user-name">{{ userName }}</h2>
    <p class="user-role">{{ currentDate }}</p>
    <nav class="menu">
      <ul>
        <li><router-link to="/dashboard">พลังงานโดยรวม</router-link></li>
        <li><router-link to="/room/Livingroom">ห้องนั่งเล่น</router-link></li>
        <li><router-link to="/room/Bedroom">ห้องนอน</router-link></li>
        <li><router-link to="/room/Kitchen">ห้องครัว</router-link></li>
        <li><router-link to="/room/Bathroom">ห้องอาบน้ำ</router-link></li>
        <li><router-link to="/report">รายงานค่าใช้จ่าย</router-link></li>
        <!-- <li><router-link to="/notification">แจ้งเตือน</router-link></li> -->
      </ul>
    </nav>
    <button class="logout-btn" @click="logout">ออกระบบ</button>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      userName: "",
    }
  },
  name: "SidebarMenu",
  computed: {
    currentDate() {
      const date = new Date();
      const day = String(date.getDate()).padStart(2, "0");
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const year = date.getFullYear().toString();
      return `${day}/${month}/${year}`;
    },
  },
  async created() {
    // ดึงข้อมูลผู้ใช้งานเมื่อ component ถูกสร้าง
    await this.fetchUserData();
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://localhost:5000/api/login', {
          username: this.username,
          password: this.password,
        });

        // เก็บ Token ลงใน localStorage
        localStorage.setItem('token', response.data.token);

        // ส่งผู้ใช้ไปยังหน้า Dashboard หรือหน้าอื่น ๆ
        this.$router.push('/dashboard');
      } catch (error) {
        console.error('Login failed:', error.response?.data || error.message);
      }
    },
    // เรียก API เพื่อดึงข้อมูลผู้ใช้งาน
    async fetchUserData() {
      try {
        const response = await axios.get("http://localhost:5000/api/user", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`, // ส่ง token สำหรับ authentication
          },
        });
        this.userName = response.data.username; // อัปเดตชื่อผู้ใช้งาน
      } catch (error) {
        console.error("Failed to fetch user data:", error.response?.data || error.message);
      }
    },
    logout() {
      localStorage.clear();
      this.$router.push("/login");
    },
  },
};
</script>

<style>
body,
html {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}

.sidebar {
  width: 250px;
  height: 100vh;
  background-color: #0057d9;
  /* สีฟ้าน้ำเงิน */
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