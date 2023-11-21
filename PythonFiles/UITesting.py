import tkinter as tk
import cv2
import os
from PIL import ImageTk, Image
from inputs import get_gamepad
from inputs import UnpluggedError
from inputs import devices
for device in devices.gamepads:
    print(device)

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
    angle = AI_Sens.get()
    Video_Angle_Update.config(text=f"Servo Angle: {angle}")

    # Update the angle label (example, you can replace it with your actual angle calculation)

def poll_controller():
    try:
        events = get_gamepad()
    
        for event in events:
            print(event.ev_type, event.code, event.state)  # Debugging print
            if event.ev_type == 'Key':
                if event.code == 'BTN_SOUTH' and event.state == 1:  # 'A' button pressed
                    current_color = AI_Label.cget("fg")
                    new_color = "green" if current_color == "red" else "red"
                    AI_Label.config(fg=new_color)
                    print("A button pressed, color changed to", new_color)  # Debugging print
    except UnpluggedError:
        print("No gamepad found. Please connect your controller.")
        # Optionally, you can re-try after a delay
        master.after(10000, poll_controller)  # Retry after 1 second
    else:
        # Schedule the next poll only if no error occurred
        master.after(100, poll_controller)    
    # Schedule the next poll
    master.after(100, poll_controller)

master = tk.Tk()
master.title('Hello')
master.geometry ("720x360")
# Configure row 0 column 0 to expand with a weight of 1
master.grid_rowconfigure(0, weight=1)
master.grid_columnconfigure(0, weight=1)
master.state('zoomed') 

#Create widgets
frame_main = tk.Frame(master,background="white")

frame_left = tk.Frame(frame_main,  width=100, bg="white")
frame_mid = tk.Frame(frame_main, bg="white")
frame_right = tk.Frame(frame_main, width=100, bg="white")

label_width = 30
label_height = 15

VideoLabel = tk.Label(frame_mid, borderwidth=3, relief="solid", bg="white")
Video_Title_Label = tk.Label(frame_mid, text="AI Feed", font=("Georgia", 16),fg="black", bg="white")
Video_Angle_Update = tk.Label(frame_mid, text="Servo Angle: 90", font=("Georgia", 16),fg="black", bg="white")
AI_Label = tk.Label(frame_mid, text='AI', width=label_width, height=label_height, 
                    borderwidth=2, relief="solid", font=("Georgia", 10), fg="red", bg="white", )

#AI_Label = tk.Label(frame_mid, text='AI', width=label_width, height=label_height, borderwidth=2, relief="solid", font=("Georgia", 10),fg="black", bg="red")
AI_Sens = tk.Scale(frame_mid, from_=0, to=180, orient="horizontal", length=300, fg="black", bg="white")
AI_Sens.set(90)
Manual_Label = tk.Label(frame_mid, text='Manual', width=label_width, height=label_height, 
                    borderwidth=2, relief="solid", font=("Georgia", 10), fg="green", bg="white", )

#AI
#Manual_Label = tk.Label(frame_mid, text='Manual', width=label_width, height=label_height, borderwidth=2, relief="solid", font=("Georgia", 10),fg="black", bg="green")
Manual_Sens = tk.Scale(frame_mid, from_=0, to=180, orient="horizontal", length=300, fg="black", bg="white")
Manual_Sens.set(90)

# Grid Widgets on the screen
frame_main.grid(row=0,column=0, sticky="ewns")
frame_main.grid_rowconfigure(0,weight=1)
# Set weights for the columns in frame_main
frame_main.grid_columnconfigure(0, weight=1)  # Column for frame_left
frame_main.grid_columnconfigure(1, weight=0)  # Column for frame_mid (no weight)
frame_main.grid_columnconfigure(2, weight=1)  # Column for frame_right

frame_left.grid(row=0, column=0,sticky="ewns")   
frame_mid.grid(row=0, column=1)
frame_right.grid(row=0, column=2, sticky="ewns")

VideoLabel.grid(row=0, column=0)
Video_Title_Label.grid(row=0, column=0, sticky='n',pady=30)
Video_Angle_Update.grid(row=0, column=0, sticky='s',pady=30)

AI_Label.grid(row=0, column=1, padx=70, pady=185, sticky="w")  
Manual_Label.grid(row=0, column=2, padx=70, pady=185, sticky="e")  

AI_Sens.grid(row=0, column=1,padx=15, pady=120, sticky="nw")
Manual_Sens.grid(row=0, column=2, padx=10, pady=120, sticky="ne")

camdisplay()
poll_controller()
master.mainloop()