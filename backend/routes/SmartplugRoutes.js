const express = require("express");
const router = express.Router();
const Smartplug = require("../models/SmartPlug"); // สมมติว่าคุณมีโมเดล Smartplug

// เพิ่ม Smartplug
router.post("/api/addsmartplugs", async (req, res) => {
  const { room, userid, email, password, ipAddress, smartplugname } = req.body;

  try {
    const newSmartplug = new Smartplug({
      room,
      userid,
      email,
      password,
      ipAddress,
      smartplugname,
    });

    await newSmartplug.save();
    res.status(201).json(newSmartplug);
  } catch (error) {
    res.status(500).json({ message: "Failed to add smartplug", error: error.message });
  }
});

module.exports = router;