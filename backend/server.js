const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const authRoutes = require("./routes/auth");
const axios = require('axios');

const app = express();
app.use(express.json());
app.use(cors());

// Import Routes
const userRoutes = require('../backend/routes/UserRoutes');
app.use(userRoutes);
const deviceRoutes = require('../backend/routes/DeviceRoutes');
app.use('/api/devices', deviceRoutes);
const smartplugRoutes = require("../backend/routes/SmartplugRoutes");
app.use(smartplugRoutes);
//Auth
app.use('/api', authRoutes);

//Tapo API
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.get('/api/energy/:room/:userid', async (req, res) => {
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

// เชื่อมต่อ MongoDB ชื่อdatabase[SmartHome]
mongoose.connect('mongodb://localhost:27017/SmartHome', {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log('✅ MongoDB Connected!'))
.catch(err => console.error('❌ MongoDB Connection Error:', err));

app.get('/', (req, res) =>{
  res.send("get connect");
});

const PORT = 5000
app.listen(5000, () => {
  console.log(`🚀 Server running o http://localhost:${PORT}`);
});