import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2
import random
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


# This is test URLs (OpenPLC API).
@app.get("/led")
def get_random_number():
    random_value = random.randint(0, 10)
    return {random_value}

@app.get("/motor")
def get_random_number():
    random_value = random.randint(-10, 10)
    return {random_value}