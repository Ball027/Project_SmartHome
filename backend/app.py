from flask import Flask, jsonify, request
from tapo import ApiClient
from tapo.requests import EnergyDataInterval
import asyncio
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson import ObjectId
import math
import schedule
import time
from threading import Thread

app = Flask(__name__)

# เชื่อมต่อ MongoDB
mongo_uri = "mongodb://localhost:27017/SmartHome"
client = MongoClient(mongo_uri)
db = client["SmartHome"]  # ชื่อ database
collection = db["SmartPlugs"]  # ชื่อ collection
power_records_collection = db["PowerRecords"]  # ชื่อ collection สำหรับบันทึกข้อมูลพลังงานรายเดือน

#ดึงenergy_usage จาก Smartplug
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

        # แปลง total_runtime จากนาทีเป็นชั่วโมง (ปัดเศษลง)
        today_runtime_hours = math.floor(today_runtime / 60)

        return {
            "plugname": plugname,
            "_id": str(_id),
            "ip_address": ip_address,
            "current_power": current_power.to_dict().get("current_power", 0),  # พลังงานปัจจุบัน วัตต์ (W)
            "today_energy": today_energy,  # พลังงานที่ใช้วันนี้ วัตต์-ชั่วโมง (Wh)
            "today_runtime": today_runtime_hours,  # เวลาที่ใช้วันนี้ ชั่วโมง
            "total_energy_month": energy_usage.to_dict().get("month_energy", 0),
            "total_runtime_month": math.floor(energy_usage.to_dict().get("month_runtime", 0) / 60),  # เวลาที่ใช้ในเดือนนี้ ชั่วโมง
            "status": True,
        }
    except Exception as e:
        print(f"Failed to fetch data from Smartplug(OFF): {e}")
        # หากดึงข้อมูลไม่สำเร็จ (อุปกรณ์ปิดอยู่หรือไม่สามารถเชื่อมต่อได้)
        return {
            "plugname": plugname,
            "_id": str(_id),
            "ip_address": ip_address,
            "current_power": 0,  # กำหนดค่าเป็น 0
            "today_energy": 0,  # กำหนดค่าเป็น 0
            "today_runtime": 0,  # กำหนดค่าเป็น 0
            "total_energy_month": 0,  # กำหนดค่าเป็น 0
            "total_runtime_month": 0,  # กำหนดค่าเป็น 0
            "status": False,
        }
#ดึงenergy_usageตามห้อง
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

            # ตรวจสอบว่าข้อมูลครบถ้วน
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
    except Exception as e:
        return jsonify({"message": "Failed to fetch energy data", "error": str(e)}), 500

#ควบคุมการ On/Off Smartplug
@app.route('/api/toggle-plug/<device_id>', methods=['PUT'])
async def toggle_plug(device_id):
    try:
        data = request.get_json()
        status = data.get("status")  # "on" หรือ "off"
        print(f"Received status: {status}")
        # ดึงข้อมูล plug จาก MongoDB
        plug = collection.find_one({"_id": ObjectId(device_id)})
        if not plug:
            return jsonify({"message": "Device not found"}), 404

        # ตรวจสอบว่าข้อมูลครบถ้วน
        email = plug.get("email")
        password = plug.get("password")
        ip_address = plug.get("ipAddress")
        plug_type = plug.get("type")

        if not all([email, password, ip_address, plug_type]):
            return jsonify({"message": "Missing credentials, IP address, or plug type"}), 400

        # เชื่อมต่อกับ Tapo plug
        client = ApiClient(email, password)
        
        # ตรวจสอบชนิดของ plug
        if plug_type == "TP-Link Tapo P110":
            device = await client.p110(ip_address)
        elif plug_type == "TP-Link Tapo P115":
            device = await client.p115(ip_address)
        else:
            return jsonify({"message": "Unknown plug type"}), 400

        # เปลี่ยนสถานะ plug
        if status == "on":
            await device.on()
        elif status == "off":
            await device.off()
        else:
            return jsonify({"message": "Invalid status"}), 400

        return jsonify({"message": f"Device turned {status}"}), 200
    except Exception as e:
        return jsonify({"message": "Failed to toggle device", "error": str(e)}), 500

def save_monthly_data():
    print("กำลังบันทึกข้อมูลทุกสิ้นเดือน...")
    try:
        # ดึงข้อมูลผู้ใช้ทั้งหมดจาก MongoDB (หรือดึงเฉพาะ userid ที่ต้องการ)
        users = list(db["Users"].find({}, {"_id": 1}))  # สมมติว่ามี collection "Users" สำหรับเก็บข้อมูลผู้ใช้

        if not users:
            print("No users found in database")
            return

        # สำหรับแต่ละผู้ใช้
        for user in users:
            userid = user["_id"]
            print(f"กำลังบันทึกข้อมูลสำหรับ userid: {userid}")

            # ดึงข้อมูล Smart Plugs ของผู้ใช้นี้
            smart_plugs = list(collection.find({"userid": userid}))

            if not smart_plugs:
                print(f"No smart plugs found for userid: {userid}")
                continue

            # เรียก Tapo API สำหรับทุก Smart Plug ของผู้ใช้นี้
            for plug in smart_plugs:
                plugname = plug.get("smartplugname")
                _id = plug.get("_id")
                email = plug.get("email")
                password = plug.get("password")
                ip_address = plug.get("ipAddress")
                room = plug.get("room")
                plug_type = plug.get("type")  # ดึงชนิดของ plug

                # ตรวจสอบว่าข้อมูลครบถ้วน
                if not all([email, password, ip_address, plug_type]):
                    print(f"Missing credentials, IP address, or plug type for {plugname}")
                    continue

                energy_data = asyncio.run(get_energy_data(plugname, _id, plug_type, email, password, ip_address))
                print(f"บันทึกข้อมูลสำหรับ {plugname}: {energy_data}")

                # ตรวจสอบว่ามีข้อมูลสำหรับเดือนนี้แล้วหรือไม่
                existing_record = power_records_collection.find_one({
                    "smartplugid": _id,
                    "date": datetime.now().strftime("%Y-%m")
                })

                if existing_record:
                    print(f"ข้อมูลสำหรับ {plugname} ในเดือนนี้ถูกบันทึกแล้ว")
                    continue

                # บันทึกข้อมูลลงในคอลเลกชัน PowerRecords
                power_records_collection.insert_one({
                    "smartplugid": _id,
                    "smartplugname": plugname,
                    "userid": userid,
                    "room": room,
                    "date": datetime.now().strftime("%Y-%m"),  # รูปแบบเดือน/ปี
                    "total_energy_month": energy_data["total_energy_month"],
                    "total_runtime_month": energy_data["total_runtime_month"],
                })

    except Exception as e:
        print(f"Failed to save monthly data: {e}")

def mock_today(mock_date=None):
    if mock_date:
        return mock_date  # ใช้ mock_date ที่ส่งมา
    return datetime.today()  # ใช้วันที่ปัจจุบันจริง

def is_last_day_of_month():
    today = mock_today()
    tomorrow = today + timedelta(days=1)
    return tomorrow.month != today.month
print(is_last_day_of_month())  # ผลลัพธ์: True
def schedule_monthly_task():
    if is_last_day_of_month():
        print(f"สิ้นเดือนแล้ว")
        save_monthly_data()

# ตั้งเวลาให้รันทุกวัน เวลา 23:59
schedule.every().day.at("23:59").do(schedule_monthly_task)

# ฟังก์ชันรัน scheduler ใน Thread แยก
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # schedule_monthly_task()ใช้ทดสอบเนื่องจากไม่สามารถรันapp.pyได้24/7
    #เพื่อไม่ให้ทำงานทับกันเพราะschedule_pendingต้องรันตลอดเวลาเพื่อเช็คเวลาที่จะถึง
    scheduler_thread = Thread(target=run_scheduler) #สร้างThreadสำหรับrun_schedule
    scheduler_thread.daemon = True  #Thread ปิดเมื่อโปรแกรมหลักปิด
    scheduler_thread.start()
    app.run(host='0.0.0.0', port=5000)