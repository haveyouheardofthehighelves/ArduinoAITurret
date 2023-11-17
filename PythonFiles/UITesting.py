import tkinter as tk
import cv2
import os
from PIL import ImageTk, Image


def close_window():
    master.destroy()


current_directory = os.getcwd()
os.chdir('../')

# Go up one directory

# Construct the path to the XML file in the parent directory
xml_file_path = os.path.join(os.getcwd(), 'XMLFILES', 'upperbody.xml')
print(xml_file_path)
# Create the CascadeClassifier
face_cascade = cv2.CascadeClassifier(xml_file_path)
cap = cv2.VideoCapture(0)


def scanbody(part, B, G, R, frame):
    for (x, y, w, h) in part:
        center_x = x + w // 2
        center_y = y + h // 2
        pos = (center_x, center_y)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (B, G, R), 3)


def camdisplay():
    _, frame = cap.read()
    height, width, _ = frame.shape
    x_origin = width / 2
    y_origin = height / 2
    origin = (x_origin, y_origin)

    # Convert into grayscales
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, 1.1, 3)
    scanbody(face, 0, 0, 255, frame)
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)
    VideoLabel.imgtk = imgtk
    VideoLabel.configure(image=imgtk)
    VideoLabel.after(20, camdisplay)


master = tk.Tk()
master.title('Hello')

C_1 = tk.Canvas(master, width=1500, height=700)
C_1.pack()

# Create a label inside the canvas
label_width = 30
label_height = 15
AI_Label = tk.Label(C_1, text='AI', width=label_width, height=label_height, borderwidth=2, relief="solid")
Manual_Label = tk.Label(C_1, text='Manual', width=label_width, height=label_height, borderwidth=2, relief="solid")
# Adjust the coordinates to place the label at the bottom left corner
AI_sens = tk.Scale(master, from_=0, to=180, orient="horizontal", length=300)
AI_sens.set(90)

VideoLabel = tk.Label(C_1)
C_1.create_window(600, 400, window=VideoLabel, anchor='center')
C_1.create_window(165, 600, window=AI_sens, anchor='sw')
C_1.create_window(100, 500, window=AI_Label, anchor='sw')
C_1.create_window(315, 500, window=Manual_Label, anchor='sw')

camdisplay()
master.mainloop()
