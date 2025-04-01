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
import os

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
            "total_energy_month": energy_usage.to_dict().get("month_energy", 0), # พลังงานที่ใช้เดือนนี้ วัตต์-ชั่วโมง (Wh)
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

#ดึงcurrent_powerของทุกห้อง
@app.route('/api/current-power/<userid>', methods=['GET'])
def get_current_power_by_room(userid):
    try:
        print(f"Received userid: {userid}")  # แสดงค่า userid
        object_userid = ObjectId(userid)

        # ดึงข้อมูล Smart Plugs จาก MongoDB
        smart_plugs = list(collection.find(
            {"userid": object_userid},
            {"_id": 1, "smartplugname": 1, "email": 1, "password": 1, "ipAddress": 1, "type": 1, "room": 1}
        ))

        if not smart_plugs:
            return jsonify({"message": "No smart plugs found in database"}), 404

        # ตัวแปรเก็บผลลัพธ์
        room_power = {
            "Livingroom": 0,  # ห้องนั่งเล่น
            "Bedroom": 0,     # ห้องนอน
            "Kitchen": 0,      # ห้องครัว
            "Bathroom": 0,     # ห้องน้ำ
        }

        # เรียก Tapo API สำหรับทุก Smart Plug
        for plug in smart_plugs:
            plugname = plug.get("smartplugname")
            _id = plug.get("_id")
            email = plug.get("email")
            password = plug.get("password")
            ip_address = plug.get("ipAddress")
            room = plug.get("room")  # ดึงชื่อห้อง
            plug_type = plug.get("type")  # ดึงชนิดของ plug

            # ตรวจสอบว่าข้อมูลครบถ้วน
            if not all([email, password, ip_address, plug_type]):
                print(f"Missing credentials, IP address, or plug type for {plugname}")
                continue

            # ดึงข้อมูล current_power
            energy_data = asyncio.run(get_energy_data(plugname, _id, plug_type, email, password, ip_address))
            current_power = energy_data.get("current_power", 0)

            # เพิ่ม current_power ไปยังห้องที่เกี่ยวข้อง
            if room in room_power:
                room_power[room] += current_power

        return jsonify(room_power)
    except Exception as e:
        return jsonify({"message": "Failed to fetch current power data", "error": str(e)}), 500

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

#คำนวนค่าไฟประจำเดือน
def calculate_electricity_cost(total_units):
    """คำนวณค่าไฟตามอัตราก้าวหน้าของการไฟฟ้าฝ่ายผลิตแห่งประเทศไทย (กฟผ.)"""
    if total_units <= 150:
        return total_units * 3.2484
    elif total_units <= 400:
        return (150 * 3.2484) + ((total_units - 150) * 4.2218)
    else:
        return (150 * 3.2484) + (250 * 4.2218) + ((total_units - 400) * 4.4217)

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

            # ตรวจสอบว่ามีข้อมูลใน Reports สำหรับเดือนนี้แล้วหรือไม่
            current_month_year = datetime.now().strftime("%Y-%m")
            existing_report = db["Reports"].find_one({
                "userid": userid,
                "month/year": current_month_year
            })

            if existing_report:
                print(f"ข้อมูลสำหรับ userid: {userid} ในเดือน {current_month_year} ถูกบันทึกแล้ว")
                continue

            # ตัวแปรเก็บข้อมูลรวม
            total_energy_user = 0  # พลังงานรวมทั้งเดือน (Wh)
            total_runtime_user = 0  # เวลาการทำงานรวมทั้งเดือน (ชั่วโมง)
            total_units_user = 0  # พลังงานรวมทั้งเดือน (kWh)
            total_cost = 0  # ค่าไฟรวมทั้งเดือน (บาท)

            # พลังงานรวมของแต่ละห้อง
            livingroom_energy = 0
            bedroom_energy = 0
            bathroom_energy = 0
            kitchen_energy = 0

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

                # ตรวจสอบว่ามีข้อมูลใน PowerRecords สำหรับ plug นี้ในเดือนนี้แล้วหรือไม่
                existing_power_record = power_records_collection.find_one({
                    "smartplugid": _id,
                    "date": current_month_year
                })

                if existing_power_record:
                    print(f"ข้อมูลสำหรับ {plugname} ในเดือน {current_month_year} ถูกบันทึกแล้ว")
                    continue

                energy_data = asyncio.run(get_energy_data(plugname, _id, plug_type, email, password, ip_address))
                print(f"บันทึกข้อมูลสำหรับ {plugname}: {energy_data}")

                # คำนวณพลังงานรวม (kWh)
                energy_wh = energy_data["total_energy_month"]  # พลังงานในหน่วย Wh
                runtime_hours = energy_data["total_runtime_month"]  # เวลาในหน่วยชั่วโมง
                units = (energy_wh / 1000)  # แปลงเป็น kWh

                # เพิ่มพลังงานรวมของผู้ใช้
                total_energy_user += energy_wh
                total_runtime_user += runtime_hours
                total_units_user += units

                # เพิ่มพลังงานรวมของแต่ละห้อง
                if room == "Livingroom":
                    livingroom_energy += energy_wh
                elif room == "Bedroom":
                    bedroom_energy += energy_wh
                elif room == "Bathroom":
                    bathroom_energy += energy_wh
                elif room == "Kitchen":
                    kitchen_energy += energy_wh

                # บันทึกข้อมูลลงในคอลเลกชัน PowerRecords
                power_records_collection.insert_one({
                    "smartplugid": _id,
                    "smartplugname": plugname,
                    "userid": userid,
                    "room": room,
                    "date": current_month_year,  # รูปแบบเดือน/ปี
                    "total_energy_month": energy_wh,
                    "total_runtime_month": runtime_hours,
                    "units": round(units, 2),  # ปัดเศษ units ให้เหลือทศนิยม 2 ตำแหน่ง
                })

            # คำนวณค่าไฟ
            total_cost = calculate_electricity_cost(total_units_user)

            # บันทึกข้อมูลลงในคอลเลกชัน Report
            db["Reports"].insert_one({
                "userid": userid,
                "month/year": current_month_year,  # รูปแบบเดือน/ปี
                "total_energy": total_energy_user,  # พลังงานรวมทั้งเดือน (Wh)
                "total_runtime": total_runtime_user,  # เวลาการทำงานรวมทั้งเดือน (ชั่วโมง)
                "total_units": round(total_units_user, 2),  # พลังงานรวมทั้งเดือน (kWh)
                "total_cost": round(total_cost, 2),  # ค่าไฟรวมทั้งเดือน (บาท)
                "livingroom_energy": livingroom_energy,  # พลังงานรวมของห้อง Living Room (Wh)
                "bedroom_energy": bedroom_energy,  # พลังงานรวมของห้อง Bedroom (Wh)
                "bathroom_energy": bathroom_energy,  # พลังงานรวมของห้อง Bathroom (Wh)
                "kitchen_energy": kitchen_energy,  # พลังงานรวมของห้อง Kitchen (Wh)
            })

    except Exception as e:
        print(f"Failed to save monthly data: {e}")

def mock_today(mock_date=None):
    if mock_date:
        return mock_date  # ใช้ mock_date ที่ส่งมา
    return datetime.today()  # ใช้วันที่ปัจจุบันจริง

def is_last_day_of_month():
    today = mock_today() #datetime(2025, 3, 31)
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
#deploy
@app.route('/python-api')
def hello():
    return jsonify({"message": "Hello from Flask API!"})
    
if __name__ == '__main__':
    #ใช้ทดสอบเนื่องจากไม่สามารถรันapp.pyได้24/7
    schedule_monthly_task()
    #เพื่อไม่ให้ทำงานทับกันเพราะschedule_pendingต้องรันตลอดเวลาเพื่อเช็คเวลาที่จะถึง
    scheduler_thread = Thread(target=run_scheduler) #สร้างThreadสำหรับrun_schedule
    scheduler_thread.daemon = True  #Thread ปิดเมื่อโปรแกรมหลักปิด
    scheduler_thread.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)