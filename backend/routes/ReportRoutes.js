// routes/ReportRoutes.js
const express = require("express");
const router = express.Router();
const { MongoClient } = require("mongodb");

// เชื่อมต่อ MongoDB
const mongoUri = "mongodb://localhost:27017/SmartHome";
const client = new MongoClient(mongoUri);

// ดึงข้อมูลรายงานสำหรับปีที่เลือก
router.get("/api/reports/", async (req, res) => {
    try {
      const year = req.query.year; // รับปีจาก query parameter
      if (!year) {
        return res.status(400).json({ message: "Year is required" });
      }
  
      await client.connect();
      const db = client.db("SmartHome");
  
      // ใช้ $regex เพื่อกรองข้อมูลตามปี
      const reports = await db.collection("Reports")
        .find({ "month/year": { $regex: `^${year}` } }) // ค้นหา "month/year" ที่ขึ้นต้นด้วยปีที่เลือก
        .toArray();
  
      if (reports.length === 0) {
        return res.status(404).json({ message: "No reports found for this year" });
      }
  
      // แปลงข้อมูลให้อยู่ในรูปแบบที่ Vue.js ต้องการ
      const result = reports.map(report => ({
        "month/year": report["month/year"],
        "total_energy": report["total_energy"],
        "total_cost": report["total_cost"],
      }));
  
      res.json(result);
    } catch (error) {
      console.error("Failed to fetch reports:", error);
      res.status(500).json({ message: "Failed to fetch reports", error: error.message });
    } finally {
      await client.close();
    }
  });

// ดึงปีที่มีข้อมูลใน Reports
router.get("/api/reports/years", async (req, res) => {
    try {
      await client.connect();
      const db = client.db("SmartHome");
  
      // ใช้ Aggregation Pipeline เพื่อแยกปีจาก "month/year"
      const years = await db.collection("Reports").aggregate([
        {
          $project: {
            year: { $substr: ["$month/year", 0, 4] } // แยก 4 ตัวแรก (ปี) จาก "month/year"
          }
        },
        {
          $group: {
            _id: "$year" // รวบรวมปีที่ไม่ซ้ำกัน
          }
        },
        {
          $sort: { _id: 1 } // เรียงลำดับปีจากน้อยไปมาก
        }
      ]).toArray();
  
      // แปลงผลลัพธ์ให้เป็น array ของปี
      const yearList = years.map(item => item._id);
  
      res.json(yearList);
    } catch (error) {
      console.error("Failed to fetch years:", error);
      res.status(500).json({ message: "Failed to fetch years", error: error.message });
    } finally {
      await client.close();
    }
  });
  

module.exports = router;