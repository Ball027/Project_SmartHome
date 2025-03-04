<template>
  <div class="signin-container">
    <h1 class="signin-title">ระบบตรวจสอบพลังงาน</h1>
    <form @submit.prevent="submitSignIn" class="signin-form">
      <div class="form-group">
        <label for="username">ชื่อผู้ใช้</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="password">รหัสผ่าน</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit" class="signin-btn">เข้าสู่ระบบ</button>
      <p class="register-text">
        ไม่มีบัญชี? <router-link to="/" class="register-link">ลงทะเบียน</router-link>
      </p>
    </form>
  </div>
</template>

<script>
export default {
  name: "SignIn",
  data() {
    return {
      signinData: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    submitSignIn() {
      if (this.username && this.password) {
        // Redirect to Dashboard
        this.$router.push("/dashboard");
      } else {
        alert("กรุณากรอกชื่อผู้ใช้และรหัสผ่าน");
      }
    },
  },
};
</script>

<style scoped>
.signin-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f9fafb;
}

.signin-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.signin-form {
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

.signin-btn {
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

.signin-btn:hover {
  background-color: #2b6cb0;
}

.register-text {
  margin-top: 15px;
  font-size: 0.9rem;
  text-align: center;
  color: #555;
}

.register-link {
  color: #3182ce;
  text-decoration: none;
  font-weight: bold;
}

.register-link:hover {
  text-decoration: underline;
}
</style>
