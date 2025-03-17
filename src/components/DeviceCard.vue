<template>
  <div>
    <div class="device-card">
      <div class="device-info">
        <h3>{{ device.plugname }}</h3>
        <p>พลังงานไฟฟ้า: {{ device.current_power }} W</p>
        <p>เวลาที่ใช้: {{ device.today_runtime }} ชม.</p>
      </div>
      <div class="device-actions">
        <label class="switch">
          <input type="checkbox" v-model="deviceStatus" @change="toggleDevice" />
          <span class="slider round"></span>
        </label>
        <button class="delete-button" @click="modalremoveDevice">🗑️</button>
      </div>
    </div>

    <!-- Modal ยืนยันการลบ -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h2>ยืนยันการลบ</h2>
        <p>คุณแน่ใจหรือไม่ว่าต้องการลบ <strong>{{ device.plugname }}</strong>?</p>
        <div class="modal-buttons">
          <button @click="deleteDevice" class="confirm-button">ยืนยัน</button>
          <button @click="showModal = false" class="cancel-button">ยกเลิก</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  props: {
    device: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      showModal: false,
      deviceStatus: this.device.status,
    };
  },
  methods: {
    async toggleDevice() {
      try {
        const newStatus = this.device.status === true ? "off":"on"; // สลับสถานะ
        const response = await axios.put(
          `http://localhost:5000/api/toggle-plug/${this.device._id}`,
          { status: newStatus }
        );
        console.log("status switch", this.deviceStatus);
        console.log("tapo turn", newStatus);
        alert(response.data.message); // แจ้งเตือนว่าสลับสถานะสำเร็จ
        this.deviceStatus = newStatus === "off" ? false: true;
        this.$emit('toggle-device', this.device._id); // ส่ง event ไปยัง Room.vue เพื่ออัปเดตสถานะ
      } catch (error) {
        this.deviceStatus === true ? true: false;
        console.error("Failed to toggle device:", error.response?.data || error.message);
        alert("Failed to toggle device");
      }
    },
    modalremoveDevice() {
      this.showModal = true;
    },
    deleteDevice() {
      this.$emit('delete-device', this.device._id);
      this.showModal = false;
    },
  },
};
</script>

<style scoped>
.device-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border: 1px solid #ddd;
  margin-bottom: 10px;
  border-radius: 5px;
}

.device-actions {
  display: flex;
  align-items: center;
}

.switch {
  position: relative;
  display: inline-block;
  width: 34px;
  height: 20px;
  margin-right: 10px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.4s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 14px;
  width: 14px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

input:checked+.slider {
  background-color: #4caf50;
}

input:checked+.slider:before {
  transform: translateX(14px);
}

.delete-button {
  background: red;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 5px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  max-width: 300px;
  width: 100%;
}

.modal-content h2 {
  margin-bottom: 10px;
}

.modal-content p {
  margin-bottom: 20px;
}

.modal-buttons {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.confirm-button {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
}

.cancel-button {
  background-color: #ccc;
  color: black;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
}
</style>