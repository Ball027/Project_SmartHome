from flask import Flask, jsonify, request
from tapo import ApiClient
from tapo.requests import EnergyDataInterval
import asyncio
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# เชื่อมต่อ MongoDB
mongo_uri = "mongodb://localhost:27017/SmartHome"
client = MongoClient(mongo_uri)
db = client["SmartHome"]  # ชื่อ database
collection = db["SmartPlugs"]  # ชื่อ collection

async def get_energy_data(plugname, email, password, ip_address,_id):
    try:
        client = ApiClient(email, password)
        device = await client.p110(ip_address)

        # ดึงข้อมูลพลังงาน
        current_power = await device.get_current_power()
        energy_usage = await device.get_energy_usage()
        today = datetime.today()
        energy_data_hourly = await device.get_energy_data(EnergyDataInterval.Hourly, today)
        today_energy = energy_usage.to_dict().get("today_energy", 0)
        today_runtime = energy_usage.to_dict().get("today_runtime", 0)

        return {
            "plugname": plugname,
            "_id": _id,
            "ip_address": ip_address,
            "current_power": current_power.to_dict().get("current_power", 0),  # พลังงานปัจจุบัน วัตต์ (W)
            "today_energy": today_energy,  # พลังงานที่ใช้วันนี้ วัตต์-ชั่วโมง (Wh)
            "today_runtime": today_runtime,  # เวลาที่ใช้วันนี้ นาที
            "total_energy_month": energy_usage.to_dict().get("month_energy", 0),
            "total_runtime_month": energy_usage.to_dict().get("month_runtime", 0)
        }
    except Exception as e:
        print(f"Failed to fetch data from Smartplug(OFF): {e}")
        # หากดึงข้อมูลไม่สำเร็จ (อุปกรณ์ปิดอยู่หรือไม่สามารถเชื่อมต่อได้)
        return {
            "plugname": plugname,
            "_id": _id,
            "ip_address": ip_address,
            "current_power": 0,  # กำหนดค่าเป็น 0
            "today_energy": 0,  # กำหนดค่าเป็น 0
            "today_runtime": 0,  # กำหนดค่าเป็น 0
            "total_energy_month": 0,  # กำหนดค่าเป็น 0
            "total_runtime_month": 0  # กำหนดค่าเป็น 0
        }

@app.route('/api/energy/<room>/<userid>', methods=['GET'])
def energy(room, userid):
    try:
        print(f"Received room: {room}, userid: {userid}")  # แสดงค่า room และ userid
        object_userid = ObjectId(userid)
        # ดึงข้อมูล Smart Plugs จาก MongoDB
        smart_plugs = list(collection.find({"room": room, "userid": object_userid}, {"_id": 1, "smartplugname": 1, "email": 1, "password": 1, "ipAddress": 1}))

        if not smart_plugs:
            return jsonify({"message": "No smart plugs found in database"}), 404

        # เรียก Tapo API สำหรับทุก Smart Plug
        results = []
        for plug in smart_plugs:
            plugname = plug.get("smartplugname")
            _id = plug.get("_id")
            email = plug.get("email")
            password = plug.get("password")
            ip_address = plug.get("ipAddress")

            if not email or not password or not ip_address:
                results.append({"ip_address": ip_address, "error": "Missing credentials or IP address"})
                continue

            energy_data = asyncio.run(get_energy_data(plugname, email, password, ip_address,_id))
            results.append(energy_data)

        return jsonify(results)
    except Exception as e:
        return jsonify({"message": "Failed to fetch energy data", "error": str(e)}), 500

@app.route('/api/smartplug/<device_id>/<action>', methods=['PUT'])
def control_tapo(device_id, action):
    try:
        print(f"Received device_id: {device_id}")
        # ค้นหาข้อมูล Smart Plug จาก MongoDB
        device = collection.find_one({"_id": ObjectId(device_id)})
        if not device:
            return jsonify({"message": "Device not found"}), 404

        email = device.get("email")
        password = device.get("password")
        ip_address = device.get("ipAddress")

        if not email or not password or not ip_address:
            return jsonify({"message": "Missing credentials or IP address"}), 400

        # เชื่อมต่อกับ Tapo P110
        client = ApiClient(email, password)
        device = asyncio.run(client.p110(ip_address))

        # ส่งคำสั่งเปิด/ปิด
        if action == "on":
            asyncio.run(device.turn_on())
            return jsonify({"message": "Device turned on"})
        elif action == "off":
            asyncio.run(device.turn_off())
            return jsonify({"message": "Device turned off"})
        else:
            return jsonify({"message": "Invalid action"}), 400
    except Exception as e:
        return jsonify({"message": "Failed to control device", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)