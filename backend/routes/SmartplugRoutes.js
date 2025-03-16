const express = require("express");
const router = express.Router();
const Smartplug = require("../models/SmartPlug"); // สมมติว่าคุณมีโมเดล Smartplug

// เพิ่ม Smartplug
router.post("/api/addsmartplugs", async (req, res) => {
  const { room, userid, email, password, ipAddress, smartplugname, type } = req.body;

  try {
    const newSmartplug = new Smartplug({
      room,
      userid,
      email,
      password,
      ipAddress,
      smartplugname,
      type,
    });

    await newSmartplug.save();
    res.status(201).json(newSmartplug);
  } catch (error) {
    res.status(500).json({ message: "Failed to add smartplug", error: error.message });
  }
});

// ลบ Smartplug
router.delete("/api/deleteplug/:device_id", async (req, res) => {
  try {
    const deviceId = req.params.device_id;
    const result = await Smartplug.deleteOne({ _id: deviceId });

    if (result.deletedCount === 1) {
      res.status(200).json({ message: "ลบอุปกรณ์สำเร็จ" });
    } else {
      res.status(404).json({ message: "Device not found" });
    }
  } catch (error) {
    res.status(500).json({ message: "Failed to delete device", error: error.message });
  }
});

module.exports = router;