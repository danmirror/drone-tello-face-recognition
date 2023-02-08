from djitellopy import Face_Recognition, Fuzzy
from djitellopy import Drone
from tkinter import *
import tkinter as tk
from tkinter import ttk
import pathlib
from PIL import ImageTk, Image
import threading

#Tello
import cv2

myDrone = Drone()
face_rec = Face_Recognition()
fuzzy = Fuzzy()

w, h = 640, 480

# PID
kp = 0.1
ki = 0.02
kd = 0.005
pid = [kp, ki, kd]
pid_prevError = 0.0
fuzzy_prevError = 0.0
one_call = False


win = Tk()
win.geometry("790x485")
win.title("Face Tracking & Recognition")
win.resizable(0,0)

bg = Image.open("ui_data/bg.png")
bg_resize = bg.resize((800,480))
bg_img = ImageTk.PhotoImage(bg_resize)
bg_pic = Label(image=bg_img)
bg_pic.image = bg_img
bg_pic.place(x= 0, y= 0)

logo = Image.open("ui_data/ugm.png")
logo_resize = logo.resize((150,140))
img = ImageTk.PhotoImage(logo_resize)
logoo = Label(image=img,background ="#FFFFFF")
logoo.image = img
logoo.place(x= 640, y= 10)

label =Label(win)
label.grid(row=0, column=0)
# cap= cv2.VideoCapture(0)
label_tul = ttk.Label(text="Pilih Wajah", background ="#FFFFFF")
label_tul.place(x=660 , y=280)


selected = tk.StringVar()
selected1 = tk.StringVar()
selected2 = tk.StringVar()
selectedX = tk.StringVar()
selectedY = tk.StringVar()
comb_index = ttk.Combobox(win,textvariable=selected, values=["Dian","Yossi","Fahmizal","Alim","Matthew"], state="readonly", width=16)
comb_index.place (x=660 , y=300)


label_x = ttk.Label(text="X =", background ="#FFFFFF")
label_x.place(x=660 , y=180)

label_y = ttk.Label(text="Y =", background ="#FFFFFF")
label_y.place(x=660 , y=230)

x_dis = Entry(
    win,
    width=8,
    font=('Arial', 14),
    textvariable=selectedX,
    )
x_dis.place(x=680, y=180)

y_dis = Entry(
    win,
    width=8,
    font=('Arial', 14),
    textvariable=selectedY,
    )
y_dis.place(x=680, y=230)


def Takeoff():
    print("Takeoff")
    myDrone.takeoff()
    

def Close():
    print("closed")
    myDrone.landing()
    win.destroy()

def Tracking():
    global pid_prevError
    global fuzzy_prevError
  
    frame = myDrone.get_frame( w, h)
    # frame = face_rec.get_frame( w, h)
    frame , info = face_rec.find_face_all(frame)
    # frame, status, info = face_rec.find_face(frame, comb_index, selectedX, selectedY)
    # if(not status):
    # 	pass
    
    pid_prevError = myDrone.tracking_face(info, w, pid, pid_prevError)
    # pid_prevError = face_rec.face_tracking(info, w, pid, pid_prevError)

    fuzzy_prevError = myDrone.fuzzy_logic_mamdani(info, h, fuzzy_prevError)

    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    label.imgtk = imgtk
    label.configure(image=imgtk, background="#FFFFFF")
    label.after(10, Tracking)

# Button for Tracking
tracking_button = Button(win, text="Tracking", height=1, width=10,
                          bg='#F2B830',
                          fg='#163e6c',
                          font=('helvetica', 12, 'bold'),
                          border=0, command=Tracking)
tracking_button.place(x=660, y=365)

takeoff = Button(win, text="TakeOff", height=1, width=10,
                          bg='#F2B830',
                          fg='#163e6c',
                          font=('helvetica', 12, 'bold'),
                          border=0, command=Takeoff)
takeoff.place(x=660, y=400)

# Button for closing
exit_button = Button(win, text="Exit", height=1, width=10,
                          bg='#F2B830',
                          fg='#163e6c',
                          font=('helvetica', 12, 'bold'),
                          border=0, command=Close)
exit_button.place(x=660, y=435)

win.mainloop()