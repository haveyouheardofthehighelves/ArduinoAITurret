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
xml_file_path = os.path.join(os.getcwd(), 'XMLFILES', 'haarcascade_frontalface_default.xml')
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
    frame = cv2.resize(frame, (600, 400))
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
    angle = 90
    Angle_Update.config(text=f"Servo Angle: {angle}")

    # Update the angle label (example, you can replace it with your actual angle calculation)

master = tk.Tk()
master.title('Hello')

# Configure row 0 to expand with a weight of 1
master.grid_rowconfigure(0, weight=1)

# Configure column 0 to expand with a weight of 1
master.grid_columnconfigure(0, weight=1)

# Create a single canvas
C_1 = tk.Canvas(master)
C_1.grid(row=0, column=0, sticky="nsew")

# Create labels inside the canvas
label_width = 30
label_height = 15
AI_sens = tk.Scale(C_1, from_=0, to=180, orient="horizontal", length=300)

AI_Label = tk.Label(C_1, text='AI', width=label_width, height=label_height, borderwidth=2, relief="solid",
                    font=("Georgia", 10))

Manual_Label = tk.Label(C_1, text='Manual', width=label_width, height=label_height, borderwidth=2, relief="solid",
                        font=("Georgia", 10))

# Create Scale widget for AI_sens
AI_sens.set(90)

# Create VideoLabel
VideoLabel = tk.Label(C_1, borderwidth=3, relief="solid")
VideoLabel.grid(row=0, column=1, padx=50, pady=50, sticky="ne")

# Create another Scale widget for Manual_Label
Manual_Sens = tk.Scale(C_1, from_=0, to=180, orient="horizontal", length=300)
Manual_Sens.set(90)

Title_Label = tk.Label(C_1, text="AI Feed", font=("Georgia", 16))
Angle_Update = tk.Label(C_1, text="Servo Angle: 90", font=("Georgia", 16))

# Create other labels and Scale using grid
AI_Label.grid(row=0, column=2, padx=50, pady=185, sticky="e")  # Adjust padx and sticky for AI_Label
Manual_Label.grid(row=0, column=3, padx=50, pady=185, sticky="e")  # Adjust padx and sticky for Manual_Label
AI_sens.grid(row=0, column=2, sticky="nw", padx=15, pady=120, columnspan=2)

Manual_Sens.grid(row=0, column=3, padx=10, pady=120, sticky="ne", columnspan=2)

Title_Label.grid(row=0, column=0, sticky='n', columnspan=2, pady=10)
Angle_Update.grid(row=0, column=0, sticky='s', columnspan=2, pady=100)

camdisplay()
master.mainloop()
