const mongoose = require('mongoose');

const SmartPlugSchema = new mongoose.Schema({
  userid: {type: mongoose.Schema.Types.ObjectId, ref: 'User',required: true,},
  smartplugname: {type: String, required: true,},
  ipAddress: {type: String, required: true,},
  power: {type: Number, default: 0,},
//   voltage: { type: Number, default: 0,},
//   current: {type: Number, default: 0,},
//   createdAt: {type: Date, default: Date.now,},
});

module.exports = mongoose.model('SmartPlug', SmartPlugSchema, 'SmartPlugs');