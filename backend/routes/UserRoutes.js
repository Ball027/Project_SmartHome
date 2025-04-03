const express = require('express');
const authMiddleware = require("../middleware/authMiddleware");
const router = express.Router();
const User = require('../models/User');

//ดึงข้อมูลusername
router.get("/api/user", authMiddleware,async (req, res) => {
    try {
      const user_id = req.user_id; 
      const user = await User.findById(user_id); 
      if (!user) {
        console.log("error");
        return res.status(404).json({ message: "ไม่พบผู้ใช้งาน"});
      }
      res.json({ 
        username: user.username, 
        user_id: user._id
      }); 
    } catch (error) {
      res.status(500).json({ message: "เกิดข้อผิดพลาด", error: error.message });
    }
  });

module.exports = router;
