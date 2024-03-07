import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2
import random
import time
from serial.tools import list_ports
from pymodbus.client import ModbusSerialClient as ModbusClient
from starlette.middleware.cors import CORSMiddleware 
from fastapi.responses import StreamingResponse
from fastapi import FastAPI

app = FastAPI()

# CORSを回避するために追加（今回の肝）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

"""
関数名：video_feed
引数　：数字
返り値：画像
説明　：指定した番号のカメラのカメラストリーミング
"""
@app.get("/camera/{num}")
def video_feed(num:int = 0):
    return StreamingResponse(generate_video(num), media_type='multipart/x-mixed-replace; boundary=frame')

"""
関数名：generate_video
引数　：数字
返り値：画像
説明　：指定した番号のカメラ画像の取得
"""
def generate_video(id = 0):
    capture = cv2.VideoCapture(id)
    while True:
        if not capture.isOpened():
            return
            # capture = cv2.VideoCapture(0)
        
        ret, frame = capture.read()
        if not ret:
            break
        
        ret, jpeg = cv2.imencode('.jpg', frame)
        byte_frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')
    capture.release()

"""
関数名：get_register_value
引数　：数字
返り値：レジスターの値
説明　：指定したレジスターの値の取得
"""
@app.get("/register/{num}")
def get_register_value(num:int = 0):
    # ポート番号の自動取得
    device_port = []
    check_list = ["Arduino", "Raspberry", "ESP32"]
    for info in list_ports.comports():
        for item in check_list:
            if item in info.description:
                device_port.append(info.device)

    # modbus通信の用意
    client = ModbusClient(method = "rtu", port=device_port[0], baudrate= 115200, timeout=0.1)
    client.connect()
    time.sleep(1.6)

    # registerの状態確認
    rr = client.read_holding_registers(address=0, count=20, slave=1)

    client.close()
    return rr.registers[num]

"""
関数名：start_coil
引数　：
返り値：メッセージ
説明　：実験を開始するためにcoilをTrueにする
"""
@app.get("/start_coil")
def start_coil():
    # ポート番号の自動取得
    device_port = []
    check_list = ["Arduino", "Raspberry", "ESP32"]
    for info in list_ports.comports():
        for item in check_list:
            if item in info.description:
                device_port.append(info.device)

    # modbus通信の用意
    client = ModbusClient(method = "rtu", port=device_port[0], baudrate= 115200, timeout=0.1)
    client.connect()
    time.sleep(1.6)

    # coilのT
    rr = client.write_coils(address=3, values=1, slave=1)

    client.close()
    return "Correct"

"""
関数名：stop_coil
引数　：
返り値：メッセージ
説明　：実験を開始するためにcoilをFalseにする
"""
@app.get("/stop_coil")
def stop_coil():
    # ポート番号の自動取得
    device_port = []
    check_list = ["Arduino", "Raspberry", "ESP32"]
    for info in list_ports.comports():
        for item in check_list:
            if item in info.description:
                device_port.append(info.device)

    # modbus通信の用意
    client = ModbusClient(method = "rtu", port=device_port[0], baudrate= 115200, timeout=0.1)
    client.connect()
    time.sleep(1.6)

    # coilのF
    rr = client.write_coils(address=3, values=0, slave=1)

    client.close()
    return "Correct"


"""
# This is test URLs (OpenPLC API).
@app.get("/led")
def get_random_number():
    random_value = random.randint(0, 10)
    return {random_value}

@app.get("/motor")
def get_random_number():
    random_value = random.randint(-10, 10)
    return {random_value}
"""
