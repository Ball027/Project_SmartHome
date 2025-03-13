const axios = require("axios");

// ข้อมูลการเชื่อมต่อ Tapo
const TAPO_IP = "192.168.2.119"; // IP address Tapo P110M
const TAPO_EMAIL = "natchanonr2546@gmail.com";
const TAPO_PASSWORD = "ball1188";
//const TAPO_TOKEN = 'fc0c00d5-CTTEF6Onx239SjcA7440KEZ';
// ขอ token สำหรับการเชื่อมต่อ
async function getTapoToken() {
  try {
    const response = await axios.post(`http://${TAPO_IP}/app`, {
      method: "login",
      params: {
        username: TAPO_EMAIL,
        password: TAPO_PASSWORD,
      },
      requestTimeMils: 0,
    });
    console.log("Login Response:", response.data); // Log response ทั้งหมด
    return response.data.result.token;
  } catch (error) {
    console.error("Failed to get Tapo token:", error.message);
    throw error;
  }
}

// ดึงข้อมูลพลังงาน
async function getTapoEnergyUsage(token) {
  try {
    const response = await axios.post(`http://${TAPO_IP}/app`, {
      method: "get_energy_usage",
      params: {},
      requestTimeMils: 0,
    }, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data.result;
  } catch (error) {
    console.error("Failed to get energy usage:", error.message);
    throw error;
  }
}

module.exports = {
  getTapoToken,
  getTapoEnergyUsage,
};