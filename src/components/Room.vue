<template>
    <div class="room-container">
        <!-- Sidebar -->
        <Sidebar />

        <!-- Main Content -->
        <main class="content">
            <h1 class="title">{{ roomTitle }}</h1>
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
                <DeviceCard 
                    v-for="device in devices" 
                    :key="device.id" 
                    :device="device" 
                    @deleteDevice="openDeleteModal"
                />
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
            deviceName: "",
            power: "",
            voltage: "",
            devices: [
                { id: 1, name: "หลอดไฟ1", power: 10, usageTime: 2, isOn: true },
                { id: 2, name: "ทีวี", power: 100, usageTime: 5, isOn: false },
                { id: 3, name: "พัดลม", power: 50, usageTime: 3, isOn: false },
            ],
        };
    },
    computed: {
        roomTitle() {
            const roomMap = {
                "living-room": "ห้องนั่งเล่น",
                bedroom: "ห้องนอน",
                kitchen: "ห้องครัว",
                bathroom: "ห้องอาบน้ำ",
            };
            return roomMap[this.$route.params.room] || "ห้องไม่พบ";
        },
        isValidInput() {
            return this.deviceName.trim() !== "" && this.power > 0 && this.usageTime > 0;
        }
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
        confirmDelete() {
            if (this.selectedDevice) {
                this.devices = this.devices.filter(device => device.id !== this.selectedDevice.id);
                this.closeDeleteModal();
            }
        },
        addDevice() {
            if (this.isValidInput) {
                this.devices.push({
                    id: Date.now(),
                    name: this.deviceName,
                    power: parseFloat(this.power),
                    usageTime: parseFloat(this.usageTime),
                    isOn: false
                });
                this.closeModal();
            }
        },
        resetForm() {
            this.deviceName = "";
            this.power = "";
            this.usageTime = "";
        }
    },
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
}

/* Popup Overlay */
.modal-overlay, .modal-del {
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
.modal, .modal-content-del {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Header */
.modal-header, .modal-header-del {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* ปุ่มปิด */
.close-btn, .close-btn-del {
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
.confirm-btn, .confirm-btn-del {
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
