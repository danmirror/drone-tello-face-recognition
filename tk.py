import cv2
import tkinter as tk
from tkinter import Label
from tkinter import Button
from PIL import Image, ImageTk

# Create the GUI window
window = tk.Tk()
window.title("Video Stream with Tkinter")
window.geometry("800x600")

# Create a label to display the video
label = Label(window, bg='black')
label.place(x=100, y=100, width=600, height=400)

# Start capturing the video stream
cap = cv2.VideoCapture(0)

# Function to update the video frame in the GUI
def update_frame():
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    img = ImageTk.PhotoImage(image=img)
    label.img = img
    label.config(image=img)
    window.after(30, update_frame)

# Function to start the video stream
def start_stream():
    update_frame()
    start_button.config(state="disabled")

# Create a start button
start_button = Button(window, text="Start", bg="red", command=start_stream)
start_button.place(x=0, y=100, width=100, height=400)

# Start the GUI event loop
window.mainloop()