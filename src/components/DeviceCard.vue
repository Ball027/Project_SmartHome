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
        <button class="delete-button" @click="removeDevice">🗑️</button>
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
      deviceStatus: this.device.status, // ใช้ local data แทน props
    };
  },
  methods: {
    async toggleDevice() {
      try {
        const newStatus = this.deviceStatus ? 'on' : 'off'; // สถานะใหม่ (สลับระหว่าง on/off)
        console.log(`Toggling device: ${this.device._id}, action: ${newStatus}`);

        // เรียก API เพื่อควบคุม Tapo P110
        const response = await axios.put(`http://localhost:5000/api/smartplug/${this.device._id}/${newStatus}`);

        if (response.status === 200) {
          // อัปเดตสถานะใน local state
          this.deviceStatus = newStatus;
          // ส่ง event ไปยัง Room.vue เพื่ออัปเดตสถานะ (ถ้าจำเป็น)
          this.$emit('toggle-device', this.device._id);
        } else {
          console.error('Failed to toggle device:', response.data);
        }
      } catch (error) {
        console.error('Failed to toggle device:', error.response?.data || error.message);
      }
    },
    removeDevice() {
      this.$emit('delete-device', this.device._id); // ส่ง event ไปยัง Room.vue เพื่อลบอุปกรณ์
    },
  },
};
</script>

<style scoped>
/* CSS styles */
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

input:checked + .slider {
  background-color: #4caf50;
}

input:checked + .slider:before {
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
</style>