const mongoose = require('mongoose');

const SmartPlugSchema = new mongoose.Schema({
  smartplugname: {type: String, required: true,},
  ipAddress: {type: String, required: true,},
  userid: {type: mongoose.Schema.Types.ObjectId, ref: 'User',required: true,},
  email: { type: String, required: true },
  password: { type: String, required: true },
  room: { type: String, required: true },
});

module.exports = mongoose.model('SmartPlug', SmartPlugSchema, 'SmartPlugs');