const express = require("express");
const router = express.Router();

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

module.exports = router;