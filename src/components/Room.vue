<template>
  <div class="room-container">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main Content -->
    <main class="content">
      <h1 class="title">{{ this.room }}</h1>
      <button @click="openModal" class="add-device-btn">เพิ่มอุปกรณ์ +</button>

      <!-- Modal เพิ่มอุปกรณ์ -->
      <div v-if="showModal" class="modal-overlay">
        <div class="modal">
          <div class="modal-header">
            <h3>เพิ่มอุปกรณ์</h3>
            <button @click="closeModal" class="close-btn">X</button>
          </div>
          <div class="modal-body">
            <input type="text" placeholder="ชื่ออุปกรณ์" v-model="deviceName" required />
            <input type="number" placeholder="พลังงานไฟฟ้า (V)" v-model="voltage" required />
            <input type="number" placeholder="กำลังไฟฟ้า (W)" v-model="power" required />
          </div>
          <div class="modal-footer">
            <button @click="addDevice" class="confirm-btn" :disabled="!isValidInput">ยืนยัน</button>
          </div>
        </div>
      </div>

      <!-- แสดงรายการอุปกรณ์ -->
      <div class="device-list">
        <DeviceCard v-for="device in devices" :key="device._id" :device="device" @toggle-device="toggleDevice"
          @delete-device="confirmDelete" />
      </div>

      <!-- Modal ยืนยันการลบ -->
      <div v-if="showDeleteModal" class="modal-del">
        <div class="modal-content-del">
          <div class="modal-header-del">
            <h3>ยืนยันการลบ</h3>
            <button @click="closeDeleteModal" class="close-btn-del">X</button>
          </div>
          <div class="modal-body-del">
            <p><b>{{ selectedDevice?.name || 'อุปกรณ์' }}</b></p>
          </div>
          <div class="modal-footer-del">
            <button @click="confirmDelete" class="confirm-btn-del">ยืนยัน</button>
            <button @click="closeDeleteModal" class="cancel-btn-del">ยกเลิก</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import Sidebar from "./SidebarMenu.vue";
import DeviceCard from "./DeviceCard.vue";
import axios from "axios";

export default {
  name: "RoomName",
  components: {
    Sidebar,
    DeviceCard
  },
  data() {
    return {
      showModal: false,
      showDeleteModal: false,
      selectedDevice: null,
      userid: localStorage.getItem("userid"),
      room: this.$route.params.room, // ดึง room จาก URL
      devices: [],
    };
  },
  computed: {
    isValidInput() {
      return this.deviceName.trim() !== "" && this.power > 0 && this.usageTime > 0;
    },
  },
  watch: {
    '$route.params.room': {
      immediate: true, // เรียกทันทีเมื่อ component ถูกสร้าง
      handler(newRoom) {
        this.room = newRoom;
        this.devices = []; // เคลียร์ devices array
        this.fetchEnergy(); // ดึงข้อมูลอุปกรณ์ใหม่
      },
    },
  },
  methods: {
    openModal() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.resetForm();
    },
    openDeleteModal(device) {
      this.selectedDevice = device;
      this.showDeleteModal = true;
    },
    closeDeleteModal() {
      this.showDeleteModal = false;
      this.selectedDevice = null;
    },
    async addDevice() {
      if (this.isValidInput) {
        try {
          const response = await axios.post('http://localhost:5000/api/devices', {
            room: this.room,
            devicename: this.deviceName,
            power: parseFloat(this.power),
            status: 'off', // เริ่มต้นด้วยสถานะปิด
            userid: this.userid,
          });
          this.devices.push(response.data); // เพิ่มอุปกรณ์ใหม่เข้าไปในรายการ
          this.closeModal();
        } catch (error) {
          console.error('Failed to add device:', error.response?.data || error.message);
        }
      }
    },
    resetForm() {
      this.deviceName = "";
      this.power = "";
    },
    async fetchEnergy() {
      console.log(this.room);
      console.log(this.userid);
      if (!this.userid) {
        console.error('User ID is missing');
        return;
      }
      try {
        const response = await axios.get(`http://localhost:5000/api/energy/${this.room}/${this.userid}`);
        this.devices = response.data; // อัปเดตข้อมูลอุปกรณ์
        console.log(this.devices);
      } catch (error) {
        console.error('Failed to fetch energy from smartplug:', error.response?.data || error.message);
      }
    },
    deleteDevice(deviceId) {
      if (confirm("คุณต้องการลบอุปกรณ์นี้ใช่หรือไม่?")) {
        this.$store.commit("removeDevice", deviceId);
      }
    },
    async toggleDevice(deviceId) {
      try {
        console.log("Device ID:", deviceId); // ตรวจสอบค่า deviceId
        if (!deviceId) {
          console.error("Device ID is undefined");
          return;
        }
        // ค้นหาอุปกรณ์โดยใช้ deviceId
        const device = this.devices.find(device => device._id === deviceId);
        if (!device) {
          console.error("Device not found:", deviceId);
          return;
        }

        // สถานะใหม่ (สลับระหว่าง on/off)
        const newStatus = device.status === 'on' ? 'off' : 'on';
        console.log("Toggling device:", deviceId, "to", newStatus);

        // เรียก API เพื่อควบคุม Tapo P110
        const response = await axios.put(`http://localhost:5000/api/smartplug/${deviceId}/${newStatus}`);

        if (response.status === 200) {
          // อัปเดตสถานะใน local state
          device.status = newStatus;
          console.log("Device toggled successfully:", deviceId, "is now", newStatus);
        } else {
          console.error('Failed to toggle device:', response.data);
        }
      } catch (error) {
        console.error('Failed to toggle device:', error.response?.data || error.message);
      }
    },
    async confirmDelete(deviceId) {
      try {
        await axios.delete(`http://localhost:5000/api/devices/${deviceId}`);
        this.devices = this.devices.filter(device => device._id !== deviceId);
      } catch (error) {
        console.error('Failed to delete device:', error.response?.data || error.message);
      }
    },
  },
  mounted() {
    this.fetchEnergy();
  }
};
</script>

<style scoped>
/* Layout */
.room-container {
  display: flex;
  height: 100vh;
}

h1 {
  text-align: center;
  padding-bottom: 30px;
}

/* Main Content */
.content {
  flex-grow: 1;
  padding: 20px;
  overflow: auto;
}

.title {
  font-size: 1.5rem;
  font-weight: bold;
}

/* ปุ่มเพิ่มอุปกรณ์ */
.add-device-btn {
  background-color: #0057d9;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.add-device-btn:hover {
  background-color: #0042a5;
}

/* รายการอุปกรณ์ */
.device-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px;
}

/* Popup Overlay */
.modal-overlay,
.modal-del {
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

/* Popup */
.modal,
.modal-content-del {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Header */
.modal-header,
.modal-header-del {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* ปุ่มปิด */
.close-btn,
.close-btn-del {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

/* Input Fields */
.modal-body input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

/* ปุ่มยืนยัน */
.confirm-btn,
.confirm-btn-del {
  background: #0057d9;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.cancel-btn-del {
  background: gray;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>