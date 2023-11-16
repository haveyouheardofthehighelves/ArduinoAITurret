import tkinter as tk


def close_window():
    master.destroy()


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
w1 = tk.Scale(master, from_=0, to=180, orient="horizontal", length=300)
w1.set(90)

C_1.create_window(165, 600, window=w1, anchor='sw')
C_1.create_window(100, 500, window=AI_Label, anchor='sw')
C_1.create_window(315, 500, window=Manual_Label, anchor='sw')

master.mainloop()
