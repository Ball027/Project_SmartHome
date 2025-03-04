<template>
    <div>
        <div v-for="(device, index) in devices" :key="index" class="device-card">
            <div class="device-info">
                <h3>{{ device.name }}</h3>
                <p>พลังงานไฟฟ้า: {{ device.power }} W</p>
                <p>เวลาที่ใช้: {{ device.usage }} ชม.</p>
            </div>
            <div class="device-actions">
                <label class="switch">
                    <input type="checkbox" v-model="device.status" />
                    <span class="slider round"></span>
                </label>
                <button class="delete-button" @click="removeDevice(index)">
                    🗑️
                </button>
            </div>
        </div>
        <!-- Modal แจ้งเตือน -->
        <div v-if="showModal" class="modal-overlay">
            <div class="modal-content">
                <h2>ยืนยันที่จะลบ</h2>
                <p>{{ devices[deviceToDelete]?.name }}</p>
                <button @click="deleteDevice" class="delete-button">ยืนยัน</button>
                <button @click="showModal = false" class="delete-button">ยกเลิก</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            devices: [
                { name: "ชื่ออุปกรณ์", power: 10, usage: 2, status: true },
                { name: "ชื่ออุปกรณ์", power: 10, usage: 2, status: false },
                { name: "ชื่ออุปกรณ์", power: 10, usage: 2, status: true },
                { name: "ชื่ออุปกรณ์", power: 10, usage: 2, status: false }
            ],
            showModal: false,
            deviceToDelete: null
        };
    },
    methods: {
        removeDevice(index) {
            this.deviceToDelete = index;
            this.showModal = true;
        },
        deleteDevice() {
            this.devices.splice(this.deviceToDelete, 1);
            this.showModal = false;
        }
    }
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
    transition: .4s;
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
    transition: .4s;
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
.delete-button{
    background-color: red;
    padding: 10px;
    margin: 10px;
}
</style>