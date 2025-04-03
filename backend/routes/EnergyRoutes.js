const express = require("express");
const router = express.Router();
const axios = require('axios');

// Route สำหรับดึง Smartplug ของห้อง
router.get('/api/energy/:room/:userid', async (req, res) => {
  try {
    const { room, userid } = req.params;  // ดึง room และ userid จาก path parameters
    console.log(`Fetching energy data for room: ${room}, userid: ${userid}`);

    // เรียก Flask API โดยส่ง room และ userid ผ่าน path parameters
    const response = await axios.get(`http://localhost:5000/api/energy/${room}/${userid}`);
    res.json(response.data);  // ส่งข้อมูลพลังงานกลับไปยัง Frontend
  } catch (error) {
    console.error('Failed to fetch energy data:', error.message);
    res.status(500).json({ message: 'Failed to fetch energy data', error: error.message });
  }
});

// Route สำหรับดึง current_power ของทุกห้อง
router.get('/api/current-power/:userid', async (req, res) => {
    try {
      const { userid } = req.params;  // ดึง userid จาก path parameters
      console.log(`Fetching current power for userid: ${userid}`);
  
      // เรียก Flask API โดยส่ง userid ผ่าน path parameters
      const response = await axios.get(`http://localhost:5000/api/current-power/${userid}`);
      res.json(response.data);  // ส่งข้อมูล current_power กลับไปยัง Frontend
    } catch (error) {
      console.error('Failed to fetch current power:', error.message);
      res.status(500).json({ message: 'Failed to fetch current power', error: error.message });
    }
  });

module.exports = router;