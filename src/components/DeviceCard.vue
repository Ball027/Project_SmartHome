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
    <!-- Modal แจ้งเตือน -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h2>ยืนยันที่จะลบ</h2>
        <p>{{ device.devicename }}</p>
        <button @click="deleteDevice" class="delete-button">ยืนยัน</button>
        <button @click="showModal = false" class="delete-button">ยกเลิก</button>
      </div>
    </div>
  </div>
</template>

<script>
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
      deviceStatus: this.device.status, // ใช้ local data แทน props
      // today_runtime: Math.floor(this.device.today_runtime/60)
    };
  },
  methods: {
    toggleDevice() {
      this.$emit('toggle-device', this.device._id); // ส่ง event ไปยัง Room.vue
    },
    removeDevice() {
      this.showModal = true; // แสดง modal ยืนยันการลบ
    },
    deleteDevice() {
      this.$emit('delete-device', this.device._id); // ส่ง event ไปยัง Room.vue
      this.showModal = false; // ปิด modal
    },
    // async fetchEnergyData() {
    //   try {
    //     const response = await axios.get('http://localhost:5000/api/energy');
    //     this.energyData = response.data;
    //   } catch (error) {
    //     console.error('Failed to fetch energy data:', error.response?.data || error.message);
    //   }
    // },
  },
  // mounted() {
  //   this.fetchEnergyData(); // ดึงข้อมูลพลังงานเมื่อ component ถูกสร้าง
  // },
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
  padding: 30px;
  border-radius: 8px;
  text-align: center;
}

.delete-button {
  background-color: red;
  padding: 10px;
  margin: 10px;
}
</style>