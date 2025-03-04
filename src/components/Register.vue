<template>
    <div class="register-container">
      <h1 class="register-title">ระบบตรวจสอบพลังงาน</h1>
      <form @submit.prevent="submitRegister" class="register-form">
        <div class="form-group">
          <label for="username">ชื่อผู้ใช้</label>
          <input type="text" id="username" v-model="username" required />
        </div>
        <div class="form-group">
          <label for="password">รหัสผ่าน</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit" class="register-btn">ลงทะเบียน</button>
        <p class="signin-text">
          มีบัญชีอยู่แล้ว? <router-link to="/login" class="signin-link">เข้าสู่ระบบ</router-link>
        </p>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: "RegisterPage",
    data() {
      return {
        registerData: {
          username: "",
          password: "",
        },
      };
    },
    methods: {
      submitRegister() {
        if (this.username && this.password) {
          alert("ลงทะเบียนสำเร็จ!");
          // สามารถเพิ่ม logic สำหรับการบันทึกข้อมูลหรือเชื่อมต่อ API ได้ที่นี่
          this.$router.push("/login");
        } else {
          alert("กรุณากรอกข้อมูลให้ครบถ้วน");
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .register-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: #f9fafb;
  }
  
  .register-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 20px;
    color: #333;
  }
  
  .register-form {
    width: 100%;
    max-width: 400px;
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  label {
    display: block;
    font-size: 1rem;
    color: #333;
    margin-bottom: 8px;
  }
  
  input {
    width: 100%;
    padding: 10px;
    font-size: 1rem;
    border: 1px solid #ddd;
    border-radius: 5px;
    box-sizing: border-box;
    background-color: #f5f5f5;
  }
  
  input:focus {
    border-color: #3182ce;
    outline: none;
  }
  
  .register-btn {
    width: 100%;
    padding: 10px;
    background-color: #3182ce;
    color: white;
    font-size: 1rem;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .register-btn:hover {
    background-color: #2b6cb0;
  }
  
  .signin-text {
    margin-top: 15px;
    font-size: 0.9rem;
    text-align: center;
    color: #555;
  }
  
  .signin-link {
    color: #3182ce;
    text-decoration: none;
    font-weight: bold;
  }
  
  .signin-link:hover {
    text-decoration: underline;
  }
  </style>
  