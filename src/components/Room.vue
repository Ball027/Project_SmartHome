<template>
  <div class="room-container">
    <Sidebar />
    <main class="content">
      <h1 class="title">{{ RoomName }}</h1>
      <button @click="openModal" class="add-device-btn">เพิ่มอุปกรณ์ +</button>
      <!-- Modal เพิ่มอุปกรณ์ -->
      <div v-if="showModal" class="modal-overlay">
        <div class="modal">
          <div class="modal-header">
            <h3>เพิ่มอุปกรณ์</h3>
            <button @click="closeModal" class="close-btn">X</button>
          </div>
          <div class="modal-body">
            <input type="text" placeholder="ชื่อ Smart Plug" v-model="smartplugname" required />
            <input type="email" placeholder="อีเมล บน Tapo App" v-model="email" required />
            <input type="password" placeholder="รหัสผ่าน" v-model="password" required />
            <input type="text" placeholder="IP Address SmartPlug" v-model="ipAddress" required />
            <select v-model="selectedPlugType" required>
              <option value="" disabled>เลือกชนิดของ Plug</option>
              <option value="TP-Link Tapo P110">TP-Link Tapo P110</option>
              <option value="TP-Link Tapo P115">TP-Link Tapo P115</option>
            </select>
          </div>
          <div class="modal-footer">
            <button @click="addDevice" class="confirm-btn">ยืนยัน</button>
          </div>
        </div>
      </div>

      <!-- แสดงรายการอุปกรณ์ -->
      <div class="device-list">
        <DeviceCard v-for="device in devices" :key="device._id" :device="device" @update-device-status="UpdateDeviceStatus" @toggle-device="updateDeviceStatus"
          @delete-device="deleteDevice" />
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
    DeviceCard,
  },
  data() {
    return {
      showModal: false,
      showDeleteModal: false,
      selectedDevice: null,
      userid: localStorage.getItem("userid"),
      room: this.$route.params.room,
      devices: [],
      email: "",
      password: "",
      ipAddress: "",
      smartplugname: "",
      selectedPlugType: "",
      interval: null,
      roomMapping:{
        "Livingroom": "ห้องนั่งเล่น",
        "Bedroom": "ห้องนอน",
        "Kitchen": "ห้องครัว",
        "Bathroom": "ห้องอาบน้ำ",
      }
    };
  },
  computed: {
    RoomName() {
      return this.roomMapping[this.room]; 
    },
  },
  watch: {
    "$route.params.room": {
      immediate: true,
      handler(newRoom) {
        this.room = newRoom;
        this.devices = [];
        this.fetchEnergy();
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
    resetForm() {
      this.smartplugname = "";
      this.email = "";
      this.password = "";
      this.ipAddress = "";
      this.selectedPlugType = "";
    },
    async addDevice() {
      if (!this.smartplugname.trim()) {
        alert("กรุณากรอกชื่อ SmartPlug");
        return;
      }
      if (!this.email.trim()) {
        alert("กรุณากรอกอีเมลที่ใช้บน Smart App");
        return;
      }
      if (!this.password.trim()) {
        alert("กรุณากรอกรหัสผ่าน");
        return;
      }
      if (!this.ipAddress.trim()) {
        alert("กรุณากรอกที่อยู่ Ipaddress ของ Smartplug");
        return;
      }
      if (!this.selectedPlugType) {
        alert("กรุณาเลือกชนิดของ Plug");
        return;
      }

      try {
        const response = await axios.post("http://localhost:5000/api/addsmartplugs", {
          room: this.room,
          userid: this.userid,
          email: this.email,
          password: this.password,
          ipAddress: this.ipAddress,
          smartplugname: this.smartplugname,
          type: this.selectedPlugType,
        });
        this.devices.push(response.data);
        this.closeModal();
      } catch (error) {
        console.error("Failed to add device:", error.response?.data || error.message);
      }
    },
    async fetchEnergy() {
      try {
        const response = await axios.get(
          `http://localhost:5000/api/energy/${this.room}/${this.userid}`
        );
        console.log(this.devices);
        this.devices = response.data;
      } catch (error) {
        console.error("Failed to fetch energy data:", error.response?.data || error.message);
      }
    },
    UpdateDeviceStatus({ id, status }) {
      const device = this.devices.find((device) => device._id === id);
      if (device) {
        device.status = status;
      }
    },
    async deleteDevice(deviceId) {
      try {
        const response = await axios.delete(
          `http://localhost:5000/api/deleteplug/${deviceId}`
        );
        alert(response.data.message); // แจ้งเตือนว่าลบสำเร็จ
        this.devices = this.devices.filter(device => device._id !== deviceId); // อัปเดต local state
      } catch (error) {
        console.error("Failed to delete device:", error.response?.data || error.message);
        alert("Failed to delete device");
      }
    },
  },
  mounted() {
    this.fetchEnergy();
    this.interval = setInterval(() => {
      this.fetchEnergy();
    }, 10000);
  },
  beforeUnmount() {
    if (this.interval) {
      clearInterval(this.interval);
    }
  },
};
</script>

<style scoped>
.room-container {
  display: flex;
  height: 100vh;
}

h1 {
  text-align: center;
  padding-bottom: 30px;
}

.content {
  flex-grow: 1;
  padding: 20px;
  overflow: auto;
}

.title {
  font-size: 1.5rem;
  font-weight: bold;
}

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

.device-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px;
}

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

.modal,
.modal-content-del {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header,
.modal-header-del {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-btn,
.close-btn-del {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.modal-body input,
.modal-body select {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
  border: 1px solid #ccc;
  box-sizing: border-box;
  background-color: white;
  font-size: 16px;
}

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