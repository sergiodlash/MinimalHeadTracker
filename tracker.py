"""
Minimal webcam head tracker -> OSC (yaw, pitch, roll in degrees).

Setup (once):
    conda env create -f environment.yml
    
Run:
    conda activate headtracker
    python tracker.py
Keys:  c = recenter (zero current pose)   q = quit
"""
import os, urllib.request
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions, vision
from pythonosc.udp_client import SimpleUDPClient

# --- settings ---------------------------------------------------------------
OSC_IP = "127.0.0.1"
OSC_PORTS = [9000, 9001]        # every port gets the same messages
OSC_ADDRESS = "/ypr"            # sends 3 floats: yaw pitch roll
SMOOTHING = 0.4                 # 0 = none, 0.9 = very smooth/laggy
SHOW_LANDMARKS = True           # draw face landmarks on the preview
MIRROR = True                   # mirror the preview (display only, OSC unaffected)
MODEL = "face_landmarker.task"
MODEL_URL = ("https://storage.googleapis.com/mediapipe-models/face_landmarker/"
             "face_landmarker/float16/1/face_landmarker.task")
# ---------------------------------------------------------------------------

if not os.path.exists(MODEL):
    print("Downloading face model...")
    urllib.request.urlretrieve(MODEL_URL, MODEL)

landmarker = vision.FaceLandmarker.create_from_options(
    vision.FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL),
        running_mode=vision.RunningMode.VIDEO,
        num_faces=1,
        output_facial_transformation_matrixes=True,
    )
)
oscs = [SimpleUDPClient(OSC_IP, port) for port in OSC_PORTS]
cap = cv2.VideoCapture(0)

smoothed = np.zeros(3)
offset = np.zeros(3)
t_ms = 0

while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        break
    t_ms += 33
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = landmarker.detect_for_video(
        mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb), t_ms)

    if result.facial_transformation_matrixes:
        R = np.array(result.facial_transformation_matrixes[0])[:3, :3]
        pitch, yaw, roll = cv2.RQDecomp3x3(R)[0]          # degrees
        raw = np.array([yaw, pitch, roll])
        smoothed = SMOOTHING * smoothed + (1 - SMOOTHING) * raw
        ypr = smoothed - offset
        for osc in oscs:
            osc.send_message(OSC_ADDRESS, [float(v) for v in ypr])

    if SHOW_LANDMARKS and result.face_landmarks:
        h, w = frame.shape[:2]
        for p in result.face_landmarks[0]:
            cv2.circle(frame, (int(p.x * w), int(p.y * h)), 1, (255, 200, 0), -1)

    if MIRROR:
        frame = cv2.flip(frame, 1)
        
    if result.facial_transformation_matrixes:
        cv2.putText(frame, "yaw %6.1f  pitch %6.1f  roll %6.1f" % tuple(ypr), 
            (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 220, 120), 1, cv2.LINE_AA)

    cv2.imshow("head tracker  (c = recenter, q = quit)", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord("c"):
        offset = smoothed.copy()

cap.release()
cv2.destroyAllWindows()