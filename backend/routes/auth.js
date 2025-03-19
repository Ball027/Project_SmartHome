const express = require("express");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
const User = require("../models/User");

const router = express.Router();

// สมัครสมาชิก
router.post("/signup", async (req, res) => {
  try {
    const { username, password } = req.body;

    // ตรวจสอบความถูกต้องของข้อมูล
    if (!username || !password) {
      return res.status(400).json({ message: "กรุณากรอกชื่อผู้ใช้และรหัสผ่าน" });
    }

    if (username.length < 3 || password.length < 6) {
      return res.status(400).json({ message: "ชื่อผู้ใช้ต้องมีความยาวอย่างน้อย 3 ตัวอักษร และรหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร" });
    }

    // เช็คว่ามี username นี้อยู่แล้วหรือยัง
    const existingUser = await User.findOne({ username });
    if (existingUser) return res.status(400).json({ message: "ชื่อผู้ใช้งาน นี้ถูกใช้แล้ว" });

    // เข้ารหัสรหัสผ่าน
    const hashedPassword = await bcrypt.hash(password, 10);

    // บันทึก user ใหม่
    const newUser = new User({ username, password: hashedPassword });
    await newUser.save();

    res.status(201).json({ message: "สมัครสมาชิกสำเร็จ!", user: { id: newUser._id, username: newUser.username } });
  } catch (error) {
    res.status(500).json({ message: "เกิดข้อผิดพลาด", error: error.message });
  }
});

// เข้าสู่ระบบ
router.post("/login", async (req, res) => {
  try {
    const { username, password } = req.body;

    if (!username || !password) {
      return res.status(400).json({ message: "กรุณากรอกชื่อผู้ใช้และรหัสผ่าน" });
    }

    const user = await User.findOne({ username });
    if (!user) return res.status(400).json({ message: "ไม่พบผู้ใช้งาน" });
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) return res.status(400).json({ message: "รหัสผ่านไม่ถูกต้อง" });

    const token = jwt.sign({ user_id: user._id }, "SECRET_KEY", { expiresIn: "1h" });
    res.json({ 
      message: "เข้าสู่ระบบสำเร็จ", 
      token, 
      user: { id: user._id, username: user.username } 
    });
    console.log({ 
      message: "เข้าสู่ระบบสำเร็จ", 
      token, 
      user: { id: user._id, username: user.username } 
    })
  } catch (error) {
    res.status(500).json({ message: "ไม่พบผู้ใช้งาน", error: error.message });
  }
});

module.exports = router;