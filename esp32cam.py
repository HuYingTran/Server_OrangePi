from imutils.video import VideoStream
import imutils
import time
import cv2
import threading

outputFrame = None
lock = threading.Lock()
vs = None

def detect_motion(frameCount):
	global vs, outputFrame, lock
	vs = VideoStream(src="http://192.168.88.137:4747/video").start()
	time.sleep(2.0)
	while True:
		frame = vs.read()
		frame = imutils.resize(frame, width=400)

		with lock:
			outputFrame = frame.copy()

def generate():
	global outputFrame, lock
	while True:
		with lock:
			if outputFrame is None:
				continue
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
			if not flag:
				continue
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')