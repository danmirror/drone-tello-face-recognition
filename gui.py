import cv2
from tkinter import *
import tkinter as tk
from tkinter import ttk
import pathlib
from PIL import ImageTk, Image

from djitellopy import Drone
from djitellopy import Face_Recognition
from controller import PID, Fuzzy

w, h = 640, 480

is_drone = True

pid_ud = PID()
pid_rl = PID()

fuzzy_ud = Fuzzy()
fuzzy_rl = Fuzzy()

if is_drone :
    myDrone = Drone()

face_rec = Face_Recognition()

def set_value():
    speed_ud = [int(ud_input1.get()), int(ud_input2.get())]
    speed_rl = [int(rl_input1.get()), int(rl_input2.get())]

    arr_min = [int(negative_input1.get()), int(negative_input2.get()), int(negative_input3.get())]
    arr_nor = [int(normal_input1.get()), int(normal_input2.get()), int(normal_input3.get())]
    arr_max = [int(positive_input1.get()), int(positive_input2.get()), int(positive_input3.get())]

    pid_ud.set(float(kp_input.get()), float(ki_input.get()), float(kd_input.get()), speed_ud)
    pid_rl.set(float(kp_input.get()), float(ki_input.get()), float(kd_input.get()), speed_rl)

    fuzzy_ud.set(arr_min, arr_nor, arr_max, speed_ud)
    fuzzy_rl.set(arr_min, arr_nor, arr_max, speed_rl)

def disable():
    tracking_button["state"] = "disabled"
    negative_input1["state"] = "disabled"
    negative_input2["state"] = "disabled"
    negative_input3["state"] = "disabled"

    normal_input1["state"] = "disabled"
    normal_input2["state"] = "disabled"
    normal_input3["state"] = "disabled"

    positive_input1["state"] = "disabled"
    positive_input2["state"] = "disabled"
    positive_input3["state"] = "disabled"

    kp_input["state"] = "disabled"
    ki_input["state"] = "disabled"
    kd_input["state"] = "disabled"

    rl_input1["state"] = "disabled"
    ud_input1["state"] = "disabled"
    rl_input2["state"] = "disabled"
    ud_input2["state"] = "disabled"
    comb_face["state"] = "disabled"
    comb_control["state"] = "disabled"

def Takeoff():

    print("Takeoff")
    takeoff_button["state"] = "disabled"
    if is_drone :
        myDrone.takeoff()

def Close():
    print("closed")
    
    if is_drone :
        myDrone.landing()
    
    win.destroy()

def Tracking():
    
    set_value()
    disable()
    if is_drone :
        frame = myDrone.get_frame( w, h)
        battery_value.set(str(myDrone.get_battery()) +"%")
    else:
        frame = face_rec.get_frame( w, h)
# 
    # frame , info = face_rec.find_face_all(frame)
    frame, info = face_rec.find_face(frame, comb_face, selectedX, selectedY)

    #right left 
    if info[0][0] != 0:
        error_rl =  w // 2 -info[0][0] 
        if control_value.get() == "PID" :
            out_rl = pid_rl.update(error_rl)
            print(" Output pid rl ", out_rl)
        else:
            out_rl = fuzzy_rl.update(error_rl)
            print(" Output fuzzy rl ", out_rl)

        if is_drone :
            myDrone.control(0, 0, 0, out_rl)
    else:
        pid_rl.clear()
        fuzzy_rl.clear()

        if is_drone :
            myDrone.clear()
    
     #top down
    if info[0][1] != 0:
        error_ud =  h // 2 -info[0][1] 
        if control_value.get() == "PID" :
            out_ud = pid_ud.update(error_ud)
            print(" Output pid ud ", out_ud)
        else:
            out_ud = fuzzy_ud.update(error_ud)
            print(" Output fuzzy ud ", out_ud)
        
        if is_drone :
            myDrone.control(0, 0, out_ud, 0)
    else:
        pid_ud.clear()
        fuzzy_ud.clear()

        if is_drone :
            myDrone.clear()

    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    label.imgtk = imgtk
    label.configure(image=imgtk, background="#FFFFFF")
    label.after(10, Tracking)



# ----------- UI ---------------
win = Tk()
win.geometry("1000x485")
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

selected = tk.StringVar()
selected1 = tk.StringVar()
selected2 = tk.StringVar()
selectedX = tk.StringVar()
selectedY = tk.StringVar()
control_value = tk.StringVar()
battery_value = tk.StringVar()

label_PID = ttk.Label(text="PID", font='Helvetica 14 bold', foreground="#aaaaaa")
label_PID.place(x=820 , y=10)
label_kp = ttk.Label(text="kp") 
label_kp.place(x=820 , y=40)
label_ki = ttk.Label(text="ki")
label_ki.place(x=820 , y=60)
label_kd = ttk.Label(text="kd")
label_kd.place(x=820 , y=80)

kp_input = tk.Entry(win)
kp_input.place(x=870, y=40, width=50) 
kp_input.insert(0, 0.1)
ki_input = tk.Entry(win)
ki_input.place(x=870, y=60, width=50)
ki_input.insert(0, 0.02)
kd_input = tk.Entry(win)
kd_input.place(x=870, y=80, width=50)
kd_input.insert(0, 0.05)


label_fuzzy = ttk.Label(text="Fuzzy", font='Helvetica 14 bold', foreground="#aaaaaa")
label_fuzzy.place(x=820 , y=120)
label_kp = ttk.Label(text="Negatif")
label_kp.place(x=820 , y=150)
label_ki = ttk.Label(text="Normal")
label_ki.place(x=820 , y=170)
label_kd = ttk.Label(text="Positif")
label_kd.place(x=820 , y=190)

negative_input1 = tk.Entry(win)
negative_input1.place(x=870, y=150, width=40)
negative_input1.insert(0, -200)
negative_input2 = tk.Entry(win)
negative_input2.place(x=910, y=150, width=40)
negative_input2.insert(0, -150)
negative_input3 = tk.Entry(win)
negative_input3.place(x=950, y=150, width=40)
negative_input3.insert(0, 0)

normal_input1 = tk.Entry(win)
normal_input1.place(x=870, y=170, width=40)
normal_input1.insert(0, -150)
normal_input2 = tk.Entry(win)
normal_input2.place(x=910, y=170, width=40)
normal_input2.insert(0, 0)
normal_input3 = tk.Entry(win)
normal_input3.place(x=950, y=170, width=40)
normal_input3.insert(0, 150)

positive_input1 = tk.Entry(win)
positive_input1.place(x=870, y=190, width=40)
positive_input1.insert(0, 0)
positive_input2 = tk.Entry(win)
positive_input2.place(x=910, y=190, width=40)
positive_input2.insert(0, 150)
positive_input3 = tk.Entry(win)
positive_input3.place(x=950, y=190, width=40)
positive_input3.insert(0, 200)


label_speed = ttk.Label(text="Speed", font='Helvetica 14 bold', foreground="#aaaaaa")
label_speed.place(x=820 , y=230)
label_rl = ttk.Label(text="RL")
label_rl.place(x=820 , y=260)
label_ud = ttk.Label(text="UD")
label_ud.place(x=820 , y=280)

rl_input1 = tk.Entry(win)
rl_input1.place(x=870, y=260, width=40)
rl_input1.insert(0, -50)
rl_input2 = tk.Entry(win)
rl_input2.place(x=910, y=260, width=40)
rl_input2.insert(0, 50)

ud_input1 = tk.Entry(win)
ud_input1.place(x=870, y=280, width=40)
ud_input1.insert(0, -50)
ud_input2 = tk.Entry(win)
ud_input2.place(x=910, y=280, width=40)
ud_input2.insert(0, 50)

label_face = ttk.Label(text="Face Selectioon", font='Helvetica 12 bold', foreground="#aaaaaa")
label_face.place(x=820 , y=350)

comb_face = ttk.Combobox(win,textvariable=selected, values=["Dian","Yossi","Fahmizal","Alim","Matthew"], state="readonly", width=16)
comb_face.current(0)
comb_face.place (x=820 , y=370)

label_control = ttk.Label(text="Control Selection", font='Helvetica 12 bold', foreground="#aaaaaa")
label_control.place(x=820 , y=400)

comb_control = ttk.Combobox(win,textvariable=control_value, values=["PID","Fuzzy"], state="readonly", width=16)
comb_control.current(0)
comb_control.place (x=820 , y=420)



label_coor = ttk.Label(text="Face Coordinate", background ="#FFFFFF", font='Helvetica 12 bold', foreground="#aaaaaa")
label_coor.place(x=660 , y=180)

label_x = ttk.Label(text="X =", background ="#FFFFFF")
label_x.place(x=660 , y=210)

label_y = ttk.Label(text="Y =", background ="#FFFFFF")
label_y.place(x=660 , y=240)

x_dis = Entry(
    win,
    width=8,
    font=('Arial', 14),
    textvariable=selectedX,
    )
x_dis.place(x=690, y=210)

y_dis = Entry(
    win,
    width=8,
    font=('Arial', 14),
    textvariable=selectedY,
    )
y_dis.place(x=690, y=240)

label_bat = ttk.Label(text="Battery", background ="#FFFFFF", font='Helvetica 12 bold', foreground="#aaaaaa")
label_bat.place(x=660 , y=280)

battery = Entry(
    win,
    width=8,
    font=('Arial', 14),
    textvariable=battery_value,
    )
battery.place(x=720, y=280, width=50)


# Button for Tracking
tracking_button = Button(win, text="Tracking", height=1, width=10,
                          bg='#F2B830',
                          fg='#163e6c',
                          font=('helvetica', 12, 'bold'),
                          border=0, command=Tracking)
tracking_button.place(x=660, y=350)

takeoff_button = Button(win, text="TakeOff", height=1, width=10,
                          bg='#F2B830',
                          fg='#163e6c',
                          font=('helvetica', 12, 'bold'),
                          border=0, command=Takeoff)
takeoff_button.place(x=660, y=380)

# Button for closing
exit_button = Button(win, text="Exit", height=1, width=10,
                          bg='#F2B830',
                          fg='#163e6c',
                          font=('helvetica', 12, 'bold'),
                          border=0, command=Close)
exit_button.place(x=660, y=410)

win.mainloop()