#!/usr/bin/env python
from importlib import import_module
from flask import Flask, render_template, Response
import cv2
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import utils
import datetime
from filelock import FileLock
import os 
def monitoring():
    print("monitoring")
    options = ObjectDetectorOptions(
        num_threads=2,
        score_threshold=0.3,
        max_results=5,
        label_allow_list=["person"],
        enable_edgetpu=False)
    detector = ObjectDetector(model_path='models/yolo.tflite', options=options)
    row_size = 20  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 255)  # red
    font_size = 1
    font_thickness = 1
    
    lock = FileLock("lock.file")

    """Video streaming generator function."""
    while True: 
        if not os.path.exists("lock.file"): 
            cap = cv2.VideoCapture(0)
            saved = False
            print("getting camera in monitor")
            while True: 
                if not os.path.exists("lock.file"): 
                    flag, frame = cap.read()
                    frame=cv2.flip(frame,0)
                    detections = detector.detect(frame)

                    if not saved and len(detections)>0: 
                        bb = detections[0].bounding_box
                        roi = frame[bb.top:bb.bottom, bb.left:bb.right]
                        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        cv2.putText(roi, current_datetime,
                                    (row_size,left_margin), cv2.FONT_HERSHEY_PLAIN,
                        font_size, text_color, font_thickness)
                        if roi.size!=0:
                            cv2.imwrite(f"images/{current_datetime}.jpg", roi)
                            saved = True
            
                    if len(detections)==0:
                        saved = False
                else:
                    cap.release()
                    break
            

monitoring()

