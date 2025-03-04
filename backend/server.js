const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const app = express();
app.use(express.json());
app.use(cors()); //api

// Import Routes
const userRoutes = require('../backend/routes/UserRoutes');
app.use('/api/users', userRoutes);
const deviceRoutes = require('../backend/routes/DeviceRoutes');
app.use('/api/devices', deviceRoutes);


// เชื่อมต่อ MongoDB ชื่อdatabase[SmartHome]
mongoose.connect('mongodb://localhost:27017/SmartHome', {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log('✅ MongoDB Connected!'))
.catch(err => console.error('❌ MongoDB Connection Error:', err));

app.listen(5000, () => {
  console.log(`🚀 Server running o http://localhost:${PORT}`);
});

