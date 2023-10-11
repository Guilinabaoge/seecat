#!/usr/bin/env python
from importlib import import_module
from flask import Flask, render_template, Response
import cv2
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import utils
import datetime
import threading
from filelock import FileLock

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(cap):
     # Initialize the object detection model
    options = ObjectDetectorOptions(
        num_threads=2,
        score_threshold=0.3,
        max_results=5,
        label_allow_list=["person"],
        enable_edgetpu=False)
    detector = ObjectDetector(model_path='models/yolo.tflite', options=options)
    saved = False
    row_size = 20  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 255)  # red
    font_size = 1
    font_thickness = 1
    
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
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

        image = utils.visualize(frame, detections)
        _, buffer = cv2.imencode('.jpg', image)
        frame_bytes = buffer.tobytes()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n--frame\r\n'


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    lock = FileLock("lock.file")
    lock.acquire()
    cap = cv2.VideoCapture(0)
    while not cap.isOpened():
        cap = cv2.VideoCapture(0)
    
    # print(cap.isOpened())
    response = Response(gen(cap),mimetype='multipart/x-mixed-replace; boundary=frame')
    def end():
        cap.release()
        print("camera released")
        lock.release()

    response.call_on_close(end)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
    
