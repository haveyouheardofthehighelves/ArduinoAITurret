import tkinter as tk
import tkinter.ttk as ttk
import cv2
import os
import XboxController
from PIL import ImageTk, Image
import threading

U_IManager = {'AI_Sens': 0, 'Manual_Sens': 0}


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


def update():
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
    VideoLabel.after(20, update)
    angle = XboxController.check.angle
    pressed = XboxController.check.start_button
    if pressed:
        if Manual_Label.cget("foreground") == "green":
            Manual_Label.config(fg="red")
            AI_Label.config(fg="green")
        else:
            Manual_Label.config(fg="green")
            AI_Label.config(fg="red")
        XboxController.check.start_button = False

    Video_Angle_Update.config(text=f"Servo Angle: {angle}")
    U_IManager['AI_Sens'] = AI_Sens.get()
    U_IManager['Manual_Sens'] = Manual_Sens.get()
    print(U_IManager)
    # Update the angle label (example, you can replace it with your actual angle calculation)


xbox_thread = threading.Thread(target=XboxController.StartGame)
xbox_thread.daemon = True  # This makes the thread exit when the main program exits
xbox_thread.start()
print("hello")
master = tk.Tk()
master.title('Hello')
master.geometry("720x360")
# Configure row 0 column 0 to expand with a weight of 1
master.grid_rowconfigure(0, weight=1)
master.grid_columnconfigure(0, weight=1)

# Create widgets
frame_main = tk.Frame(master, background="white")

frame_left = tk.Frame(frame_main, width=100, bg="white")
frame_mid = tk.Frame(frame_main, bg="white")
frame_right = tk.Frame(frame_main, width=100, bg="white")

label_width = 30
label_height = 15

VideoLabel = tk.Label(frame_mid, borderwidth=3, relief="solid", bg="white")
Video_Title_Label = tk.Label(frame_mid, text="AI Feed", font=("Georgia", 16), fg="black", bg="white")
Video_Angle_Update = tk.Label(frame_mid, text="Servo Angle: 90", font=("Georgia", 16), fg="black", bg="white")

# ["aqua", "step", "clam", "alt", "default", "classic"]
style = ttk.Style()
style.configure("aqua", bordercolor="blue")

Manual_Label = tk.Label(frame_mid, text='Manual', width=label_width, height=label_height, borderwidth=2, relief="solid",
                        font=("Georgia", 10), fg="green", bg="white")

Manual_Sens = tk.Scale(frame_mid, from_=0, to=180, orient="horizontal", length=300, fg="black", bg="white")
Manual_Sens.set(90)

AI_Label = tk.Label(frame_mid, text='AI', width=label_width, height=label_height, borderwidth=2, relief="solid",
                    font=("Georgia", 10), fg="red", bg="white")

AI_Sens = tk.Scale(frame_mid, from_=0, to=180, orient="horizontal", length=300, fg="black", bg="white")
AI_Sens.set(90)

# Grid Widgets on the screen
frame_main.grid(row=0, column=0, sticky="ewns")
frame_main.grid_rowconfigure(0, weight=1)
# Set weights for the columns in frame_main
frame_main.grid_columnconfigure(0, weight=1)  # Column for frame_left
frame_main.grid_columnconfigure(1, weight=0)  # Column for frame_mid (no weight)
frame_main.grid_columnconfigure(2, weight=1)  # Column for frame_right

frame_left.grid(row=0, column=0, sticky="ewns")
frame_mid.grid(row=0, column=1)
frame_right.grid(row=0, column=2, sticky="ewns")

Manual_Label.grid(row=0, column=1, padx=70, pady=185, sticky="w")
AI_Label.grid(row=0, column=2, padx=70, pady=185, sticky="e")

Manual_Sens.grid(row=0, column=1, padx=15, pady=120, sticky="nw")
AI_Sens.grid(row=0, column=2, padx=10, pady=120, sticky="ne")

VideoLabel.grid(row=0, column=0)
Video_Title_Label.grid(row=0, column=0, sticky='n', pady=30)
Video_Angle_Update.grid(row=0, column=0, sticky='s', pady=30)

update()
master.mainloop()
