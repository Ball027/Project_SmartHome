const express = require('express');
const router = express.Router();
const Device = require('../models/Device'); // เรียกใช้ Model ของ Device

// ดึงข้อมูล Devices ทั้งหมด
router.get('/:userid/:room', async (req, res) => {
  try {
      const { userid, room } = req.params; // รับค่า userid และ room จาก URL Params
      const devices = await Device.find({ userid, room }); // ค้นหาอุปกรณ์ตามเงื่อนไข
      res.json(devices);
  } catch (error) {
      res.status(500).json({ message: 'Error fetching devices', error });
  }
});

module.exports = router;
