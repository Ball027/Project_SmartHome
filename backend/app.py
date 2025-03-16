from flask import Flask, jsonify, request
from tapo import ApiClient
from tapo.requests import EnergyDataInterval
import asyncio
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
import math  # สำหรับการปัดเศษ

app = Flask(__name__)

# เชื่อมต่อ MongoDB
mongo_uri = "mongodb://localhost:27017/SmartHome"
client = MongoClient(mongo_uri)
db = client["SmartHome"]  # ชื่อ database
collection = db["SmartPlugs"]  # ชื่อ collection

async def get_energy_data(plugname, _id, plug_type, email, password, ip_address):
    try:
        client = ApiClient(email, password)
        
        # ตรวจสอบชนิดของ plug
        if plug_type == "TP-Link Tapo P110":
            device = await client.p110(ip_address)
        elif plug_type == "TP-Link Tapo P115":
            device = await client.p115(ip_address)
        else:
            raise ValueError(f"Unknown plug type: {plug_type}")

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
            "today_runtime": math.floor(today_runtime / 60),  # เวลาที่ใช้วันนี้ นาที
            # "total_energy_month": energy_usage.to_dict().get("month_energy", 0),
            # "total_runtime_month": energy_usage.to_dict().get("month_runtime", 0)  # เวลาที่ใช้วันนี้ ชั่วโมง (ปัดเศษลง)
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
            # "total_energy_month": 0,  # กำหนดค่าเป็น 0
            # "total_runtime_month": 0  # กำหนดค่าเป็น 0
        }

@app.route('/api/energy/<room>/<userid>', methods=['GET'])
def energy(room, userid):
    try:
        print(f"Received room: {room}, userid: {userid}")  # แสดงค่า room และ userid
        object_userid = ObjectId(userid)
        # ดึงข้อมูล Smart Plugs จาก MongoDB
        smart_plugs = list(collection.find(
            {"room": room, "userid": object_userid},
            {"_id": 1, "smartplugname": 1, "email": 1, "password": 1, "ipAddress": 1, "type": 1}
        ))

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
            plug_type = plug.get("type")  # ดึงชนิดของ plug

            if not all([email, password, ip_address, plug_type]):
                results.append({
                    "plugname": plugname,
                    "ip_address": ip_address,
                    "error": "Missing credentials, IP address, or plug type"
                })
                continue


            energy_data = asyncio.run(get_energy_data(plugname, _id, plug_type, email, password, ip_address))
            results.append(energy_data)

        return jsonify(results)
        print(f"Results: {results}")
    except Exception as e:
        return jsonify({"message": "Failed to fetch energy data", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)