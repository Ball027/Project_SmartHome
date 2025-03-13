<template>
  <div class="register-container">
    <h1 class="register-title">ระบบตรวจสอบพลังงาน</h1>
    <form @submit.prevent="signup" class="register-form">
      <div class="form-group">
        <label for="username">ชื่อผู้ใช้</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="password">รหัสผ่าน</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit" class="register-btn" :disabled="isLoading">
        {{ isLoading ? "กำลังลงทะเบียน..." : "ลงทะเบียน" }}
      </button>
      <p class="signin-text">
        มีบัญชีอยู่แล้ว? <router-link to="/login" class="signin-link">เข้าสู่ระบบ</router-link>
      </p>
    </form>
  </div>
</template>

<script>
import { useStore } from "vuex";
import { ref } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "RegisterPage",
  setup() {
    const store = useStore();
    const router = useRouter();
    const username = ref("");
    const password = ref("");
    const error = ref("");
    const isLoading = ref(false);

    const signup = async () => {
      if (username.value.length < 3 || password.value.length < 6) {
        alert("ชื่อผู้ใช้ต้องมีความยาวอย่างน้อย 3 ตัวอักษร และรหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร");
        return;
      }

      isLoading.value = true;
      error.value = "";

      try {
        const success = await store.dispatch("auth/signup", { username: username.value, password: password.value });
        if (success){
          alert("ลงทะเบียนสำเร็จ");
          router.push("/login");
        }
      } catch (err) {
        const errorMessage = err.message || "การลงทะเบียนล้มเหลว กรุณาลองอีกครั้ง";
        alert(errorMessage);
      } finally {
        isLoading.value = false;
      }
    };

    return { username, password, signup, error, isLoading };
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

.register-btn:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.register-btn:hover:not(:disabled) {
  background-color: #2b6cb0;
}

.error-message {
  color: #e53e3e;
  font-size: 0.9rem;
  margin-top: 10px;
  text-align: center;
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