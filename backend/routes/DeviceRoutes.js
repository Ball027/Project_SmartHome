const express = require('express');
const router = express.Router();
const Device = require('../models/Device'); // นำเข้า Device model

// API สำหรับดึงข้อมูลอุปกรณ์โดย filter จาก room และ userid
router.get('/', async (req, res) => {
  try {
    const { room, userid } = req.query;

    // ตรวจสอบว่า room และ userid ถูกส่งมาหรือไม่
    if (!room || !userid) {
      return res.status(400).json({ message: 'กรุณาระบุ room และ userid' });
    }

    // ดึงข้อมูลอุปกรณ์จาก MongoDB โดย filter จาก room และ userid
    const devices = await Device.find({ room, userid });

    res.json(devices);
  } catch (error) {
    res.status(500).json({ message: 'เกิดข้อผิดพลาด', error: error.message });
  }
});

module.exports = router;