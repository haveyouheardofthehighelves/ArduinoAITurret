import cv2
import math
import serial
import time
import numpy as np
import os
import threading

# Get the current working directory
current_directory = os.getcwd()
os.chdir('../')

# Go up one directory

# Construct the path to the XML file in the parent directory
xml_file_path = os.path.join(os.getcwd(), 'XMLFILES', 'haarcascade_frontalface_default.xml')
print(xml_file_path)
# Create the CascadeClassifier
face_cascade = cv2.CascadeClassifier(xml_file_path)
cap = cv2.VideoCapture(0)
x_origin = 0

ser = serial.Serial("COM3", 9600, timeout=1)
serial_lock = threading.lock()

# Read the input image
def writetoarduino(writeall):
    with serial_lock:
        arr = bytes(writeall, 'utf-8')
        ser.write(arr)


def prepare_motors():
    writetoarduino('1m')


def shoot():
    while True:
        writetoarduino('1m')
        time.sleep(2)
        writetoarduino('1p')
        time.sleep(.1)
        writetoarduino('0p')
        writetoarduino('0m')


def scanbody(part, B, G, R):
    for (x, y, w, h) in part:
        center_x = x + w // 2
        center_y = y + h // 2
        pos = [center_x, center_y]
        servoX = np.interp(center_x, [0, 640], [0, 100])
        writetoarduino(f'{135 - math.floor(servoX)}s')
        # Calculate the distance from the origin to the center of the face
        # distance_to_origin = math.sqrt((center_x - 320) ** 2 + (center_y - 240) ** 2)


time.sleep(5)
thread = threading.Thread(target=shoot)
thread.daemon = True  # make the thread trminate when the main program exits
thread.start()

while True:
    _, img = cap.read()
    height, width, _ = img.shape
    x_origin = width / 2
    y_origin = height / 2
    origin = (x_origin, y_origin)

    # Convert into grayscales
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, 1.1, 3)
    if len(face) == 1:
        scanbody(face, 0, 0, 255)
    # Display the output
    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
