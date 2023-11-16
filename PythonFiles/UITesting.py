import tkinter as tk


def close_window():
    master.destroy()


master = tk.Tk()
master.title('Hello')

C_1 = tk.Canvas(master, width=1500, height=900)
C_1.pack()

# Create a label inside the canvas
label_width = 30
label_height = 15
AI_Label = tk.Label(C_1, text='AI', width=label_width, height=label_height, borderwidth=2, relief="solid")
Manual_Label = tk.Label(C_1, text='Manual', width=label_width, height=label_height, borderwidth=2, relief="solid")
# Adjust the coordinates to place the label at the bottom left corner
C_1.create_window(100, 500, window=AI_Label, anchor='sw')
C_1.create_window(315, 500, window=Manual_Label, anchor='sw')

master.mainloop()
