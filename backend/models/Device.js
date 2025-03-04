const mongoose = require('mongoose');

const deviceSchema = new mongoose.Schema({
  room: { type: String, required: true }, // ห้องที่อุปกรณ์อยู่
  devicename: { type: String, required: true }, // ชื่ออุปกรณ์
  power: { type: Number, required: true }, // กำลังไฟ
  status: { type: String, enum: ['on', 'off'], required: true }, // สถานะ เปิด/ปิด
  update: { type: Date, default: Date.now }, // เวลาที่อัปเดตล่าสุด
  userid: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true } // เชื่อมกับ User
});

const Device = mongoose.model('Device', deviceSchema, 'Devices');
module.exports = Device;
