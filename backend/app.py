from flask import Flask, jsonify, request
from tapo import ApiClient
from tapo.requests import EnergyDataInterval
import asyncio
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)

# เชื่อมต่อ MongoDB
mongo_uri = "mongodb://localhost:27017/SmartHome"
client = MongoClient(mongo_uri)
db = client["SmartHome"]  # ชื่อ database
collection = db["SmartPlugs"]  # ชื่อ collection

async def get_energy_data(plugname, email, password, ip_address):
    try:
        client = ApiClient(email, password)
        device = await client.p110(ip_address)

        # ดึงข้อมูลพลังงาน
        current_power = await device.get_current_power()
        energy_usage = await device.get_energy_usage()
        today = datetime.today()
        energy_data_hourly = await device.get_energy_data(EnergyDataInterval.Hourly, today)

        return {
            "plugname": plugname,
            "ip_address": ip_address,
            "current_power": current_power.to_dict().get("current_power", 0),  # พลังงานปัจจุบัน วัตต์ (W)
            "today_energy": energy_usage.to_dict().get("today_energy", 0),  # พลังงานที่ใช้วันนี้ วัตต์-ชั่วโมง (Wh)
            "today_runtime": energy_usage.to_dict().get("today_runtime", 0),  # เวลาที่ใช้วันนี้ นาที
        }
    except Exception as e:
        return {"ip_address": ip_address, "error": str(e)}

@app.route('/api/energy/<room>/<userid>', methods=['GET'])
def energy(room, userid):
    try:
        print(f"Received room: {room}, userid: {userid}")  # แสดงค่า room และ userid

        # ดึงข้อมูล Smart Plugs จาก MongoDB
        smart_plugs = list(collection.find({"room": room, "userid": userid}, {"_id": 0, "email": 1, "password": 1, "ipAddress": 1}))

        if not smart_plugs:
            return jsonify({"message": "No smart plugs found in database"}), 404

        # เรียก Tapo API สำหรับทุก Smart Plug
        results = []
        for plug in smart_plugs:
            plugname = plug.get("smartplugname")
            email = plug.get("email")
            password = plug.get("password")
            ip_address = plug.get("ipAddress")

            if not email or not password or not ip_address:
                results.append({"ip_address": ip_address, "error": "Missing credentials or IP address"})
                continue

            energy_data = asyncio.run(get_energy_data(plugname, email, password, ip_address))
            results.append(energy_data)

        return jsonify(results)
    except Exception as e:
        return jsonify({"message": "Failed to fetch energy data", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)