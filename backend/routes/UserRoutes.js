const express = require('express');
const router = express.Router();
const User = require('../models/User');

//ดึงข้อมูลผู้ใช้ทั้งหมด
router.get('/', async (req, res) => {
    try{
        const users = await User.find();
        console.log(users);
        res.json(users);
    }catch(error){
        res.status(500).json({message: error.message});
    }
});

module.exports = router;
