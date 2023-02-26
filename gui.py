import cv2
from tkinter import *
import tkinter as tk
from tkinter import ttk
import pathlib
from PIL import ImageTk, Image

from djitellopy import Drone
from djitellopy import Face_Recognition
from controller import PID, Fuzzy

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


is_drone = False
is_face_selection = False

state_running = False

pid_ud = PID()
pid_rl = PID()

if is_drone :
    myDrone = Drone()

face_rec = Face_Recognition()

w, h = 640, 480

# data
x_rl = np.linspace(0,10,50)
y_target_rl = np.zeros(len(x_rl))
y_error_rl = np.zeros(len(x_rl))

x_ud = np.linspace(0,10,50)
y_target_ud = np.zeros(len(x_ud))
y_error_ud = np.zeros(len(x_ud))

def set_value():
    speed_ud = [int(ud_input1.get()), int(ud_input2.get())]
    speed_rl = [int(rl_input1.get()), int(rl_input2.get())]

    pid_ud.set(float(kp_input.get()), float(ki_input.get()), float(kd_input.get()), speed_ud)
    pid_rl.set(float(kp_input.get()), float(ki_input.get()), float(kd_input.get()), speed_rl)

def disable():

    kp_input["state"] = "disabled"
    ki_input["state"] = "disabled"
    kd_input["state"] = "disabled"

    rl_input1["state"] = "disabled"
    ud_input1["state"] = "disabled"
    rl_input2["state"] = "disabled"
    ud_input2["state"] = "disabled"
    comb_face["state"] = "disabled"


def enable():
    kp_input["state"] = "normal"
    ki_input["state"] = "normal"
    kd_input["state"] = "normal"

    rl_input1["state"] = "normal"
    ud_input1["state"] = "normal"
    rl_input2["state"] = "normal"
    ud_input2["state"] = "normal"
    comb_face["state"] = "normal"

def Takeoff():
    global state_running
    if not state_running: 
        print("Takeoff")
        
        if is_drone :
            myDrone.takeoff()

        landing_button["state"] = "normal"
        takeoff_button["state"] = "disabled"
        tracking_button["state"] = "normal"
        
        set_value()
        disable()
        state_running = True

def Landing():
    global state_running
    if state_running:
        print("Landing")

        if is_drone :
            myDrone.landing()
        
        takeoff_button["state"] = "normal"
        landing_button["state"] = "disabled"
        tracking_button["state"] = "disabled"
        enable()
        state_running = False

def Close():
    print("closed")
    
    if is_drone :
        myDrone.landing()
    
    win.destroy()

def Tracking():
    
    global y_target_rl, y_error_rl, y_target_ud, y_error_ud, state_running
    if state_running:
        if is_drone :
            frame = myDrone.get_frame( w, h)
            battery_value.set(str(myDrone.get_battery()) +"%")
        else:
            frame = face_rec.get_frame( w, h)

        if is_face_selection:
            frame, info = face_rec.find_face(frame, comb_face, selectedX, selectedY)
        else:
            frame , info = face_rec.find_face_all(frame)

        #right left 
        if info[0][0] != 0:

            error_rl =  w // 2 -info[0][0] 
            
            out_rl = pid_rl.update(error_rl)
            # print(" Output pid rl ", out_rl)

            if is_drone :
                myDrone.control(0, 0, 0, out_rl)
            
            y_target_rl = np.append(y_target_rl, 0)
            y_target_rl = np.delete(y_target_rl, 0)
            y_error_rl = np.append(y_error_rl, error_rl)
            y_error_rl = np.delete(y_error_rl, 0)

        else:
            # pid_rl.clear()

            if is_drone :
                myDrone.clear()
        
        #top down
        if info[0][1] != 0:
            error_ud =  h // 2 -info[0][1] 
            out_ud = pid_ud.update(error_ud)
            # print(" Output pid ud ", out_ud)
            
            if is_drone :
                myDrone.control(0, 0, out_ud, 0)
            
            y_target_ud = np.append(y_target_ud, 0)
            y_target_ud = np.delete(y_target_ud, 0)
            y_error_ud = np.append(y_error_ud, error_ud)
            y_error_ud = np.delete(y_error_ud, 0)

        else:
            # pid_ud.clear()

            if is_drone :
                myDrone.clear()

        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk, background="#FFFFFF")
        label.after(10, Tracking)



# ----------- UI ---------------
win = Tk()
win.geometry("1200x660")
win.title("Face Tracking & Recognition")
win.resizable(0,0)


selected = tk.StringVar()
selected1 = tk.StringVar()
selected2 = tk.StringVar()
selectedX = tk.StringVar()
selectedY = tk.StringVar()
control_value = tk.StringVar()
battery_value = tk.StringVar()

############################### Title ###############################
frame_title =Frame(height = 150,width = 680,bg = "#FFFFFF", padx=10, pady=10)
frame_title.place(x= 5, y= 5)

logo = Image.open("ui_data/ugm.png")
logo_resize = logo.resize((150,140))
img = ImageTk.PhotoImage(logo_resize)
logoo = Label(frame_title, image=img,background ="#FFFFFF")
logoo.image = img
logoo.place(x= 0, y= 0)
label_title = Label(frame_title, text="IMPLEMENTASI KENDALI PID PADA\n"
                    "QUADCOPTER UNTUK STABILISASI TRACKING\n"
                    "PADA SISTEM DETEKSI WAJAH MANUSIA\n"
                    "DENGAN METODE LBPH FACE RECOGNITION",
                     fg="#aaaaaa", bg = "#FFFFFF", font="Helvetica 14 bold", width=50, height=5, anchor=CENTER)
label_title.place(x= 150, y= 0)

############################### Description ###############################
frame_des =Frame(height = 150,width = 500,bg = "#FFFFFF", padx=30, pady=30)
frame_des.place(x= 690, y= 5)
label_des = Label(frame_des, text="Dirancang Oleh:\n"
                    "Nama : Yossi Hasanah Putri A.Md.T\n"
                    "NIM : 12/483718/SV/2077\n"
                    "Prodi : Teknologi Rekayasa Instrumentasi dan Kontrol",
                     fg="#aaaaaa",bg = "#FFFFFF", font="Helvetica 12", width=60, height=5, anchor=NW, justify="left")
label_des.place(x= 0, y= 0)

############################### Image   ###############################
frame_container_img =Frame(height = h,width = w, bg = "#FFFFFF")
frame_container_img.place(x= 0, y= 160)

frame_image =Frame(height = h,width = w)
frame_image.place(x= 0, y= 160)

label =Label(frame_image)
label.grid(row=0, column=0)


############################### Face    ###############################
frame_face =Frame(height = 60,width = 120,bg = "#FFFFFF", padx=5, pady=5)
frame_face.place(x= 650, y= 180)

label_face = ttk.Label(frame_face, text="Face Selection", font='Helvetica 12 bold', background="#FFFFFF", foreground="#aaaaaa")
label_face.place(x=0 , y=0)

comb_face = ttk.Combobox(frame_face,textvariable=selected, values=["Dian","Yossi","Fahmizal","Alim","Matthew"], state="readonly", width=10)
comb_face.current(0)
comb_face.place (x=0 , y=20)

############################### Battery ###############################
frame_bat =Frame(height = 40,width = 120,bg = "#FFFFFF", padx=5, pady=5)
frame_bat.place(x= 650, y= 260)
label_bat = ttk.Label(frame_bat, text="Battery", font='Helvetica 12 bold', background="#FFFFFF", foreground="#aaaaaa")
label_bat.place(x=0 , y=0)

battery = Entry(frame_bat,width=8, font=('Arial', 14),textvariable=battery_value)
battery.place(x=60, y=0, width=40)



############################### Speed   ###############################
frame_speed =Frame(height = 160,width = 120,bg = "#FFFFFF", padx=5, pady=5)
frame_speed.place(x= 650, y= 320)

label_speed = ttk.Label(frame_speed, text="Speed", font='Helvetica 12 bold', background="#FFFFFF", foreground="#aaaaaa")
label_speed.place(x=0 , y=0)
label_U = ttk.Label(frame_speed, text="UP", background="#FFFFFF", foreground="#aaaaaa")
label_U.place(x=0 , y=20)
label_D = ttk.Label(frame_speed, text="DOWN", background="#FFFFFF", foreground="#aaaaaa")
label_D.place(x=0 , y=50)
label_R = ttk.Label(frame_speed, text="RIGHT", background="#FFFFFF", foreground="#aaaaaa")
label_R.place(x=0 , y=80)
label_L = ttk.Label(frame_speed, text="LEFT", background="#FFFFFF", foreground="#aaaaaa")
label_L.place(x=0 , y=110)

ud_input1 = tk.Entry(frame_speed)
ud_input1.place(x=60, y=20, width=40)
ud_input1.insert(0, -50)
ud_input2 = tk.Entry(frame_speed)
ud_input2.place(x=60, y=50, width=40)
ud_input2.insert(0, 50)

rl_input1 = tk.Entry(frame_speed)
rl_input1.place(x=60, y=80, width=40)
rl_input1.insert(0, -50)
rl_input2 = tk.Entry(frame_speed)
rl_input2.place(x=60, y=110, width=40)
rl_input2.insert(0, 50)

############################### PID     ###############################
frame_pid =Frame(height = 150, width = 140,bg = "#FFFFFF", padx=5, pady=5)
frame_pid.place(x= 780, y= 180)

label_PID = ttk.Label(frame_pid, text="PID", font='Helvetica 12 bold', background="#FFFFFF", foreground="#aaaaaa")
label_PID.place(x=0 , y=0)
label_kp = ttk.Label(frame_pid, text="kp", background="#FFFFFF", foreground="#aaaaaa") 
label_kp.place(x=0 , y=30)
label_ki = ttk.Label(frame_pid, text="ki", background="#FFFFFF", foreground="#aaaaaa")
label_ki.place(x=0 , y=60)
label_kd = ttk.Label(frame_pid, text="kd", background="#FFFFFF", foreground="#aaaaaa")
label_kd.place(x=0 , y=90)

kp_input = tk.Entry(frame_pid)
kp_input.place(x=30, y=30, width=80) 
kp_input.insert(0, 0.1)
ki_input = tk.Entry(frame_pid)
ki_input.place(x=30, y=60, width=80)
ki_input.insert(0, 0.02)
kd_input = tk.Entry(frame_pid)
kd_input.place(x=30, y=90, width=80)
kd_input.insert(0, 0.05)


############################### Face Coordinate   ###############################
frame_coor =Frame(height = 130, width = 140,bg = "#FFFFFF", padx=5, pady=5)
frame_coor.place(x= 780, y= 350)
label_coor = ttk.Label(frame_coor, text="Face Coordinate", background ="#FFFFFF", font='Helvetica 12 bold', foreground="#aaaaaa")
label_coor.place(x=0 , y=0)

label_x = ttk.Label(frame_coor, text="X =", background ="#FFFFFF")
label_x.place(x=0 , y=30)

label_y = ttk.Label(frame_coor, text="Y =", background ="#FFFFFF")
label_y.place(x=0 , y=65)

x_dis = Entry(frame_coor, width=8, font=('Arial', 14), textvariable=selectedX)
x_dis.place(x=30, y=30)

y_dis = Entry( frame_coor, width=8, font=('Arial', 14),textvariable=selectedY)
y_dis.place(x=30, y=65)


# Button for Tracking
tracking_button = Button(win, text="Tracking", state="disable", height=1, width=10,bg='#F2B830',fg='#163e6c',font=('helvetica', 12, 'bold'), border=0, command=Tracking)
tracking_button.place(x=660, y=530)

takeoff_button = Button(win, text="TakeOff", height=1, width=10, bg='#F2B830', fg='#163e6c', font=('helvetica', 12, 'bold'), border=0, command=Takeoff)
takeoff_button.place(x=780, y=530)

landing_button = Button(win, text="Landing",state="disable", height=1, width=10, bg='#F2B830', fg='#163e6c', font=('helvetica', 12, 'bold'), border=0, command=Landing)
landing_button.place(x=900, y=530)

# Button for closing
exit_button = Button(win, text="Exit", height=1, width=10,  bg='#F2B830', fg='#163e6c', font=('helvetica', 12, 'bold'), border=0, command=Close)
exit_button.place(x=1020, y=530)


fig_rl = plt.Figure(figsize=(3.5, 2), dpi=70)
axis_rl = fig_rl.add_subplot(1, 1, 1)
target_rl, = axis_rl.plot(x_rl, y_target_rl, color='blue', label='target 1')
error_rl, = axis_rl.plot(x_rl, y_error_rl, color='red', label='error 1')
axis_rl.legend(["target", "koreksi"], loc ="lower right")
axis_rl.title.set_text("Grafik Yaw")

fig_ud = plt.Figure(figsize=(3.5, 2), dpi=70)
axis_ud = fig_ud.add_subplot(1, 1, 1)
target_ud, = axis_ud.plot(x_ud, y_target_ud, color='blue', label='target 1')
error_ud, = axis_ud.plot(x_ud, y_error_ud, color='red', label='error 1')
axis_ud.legend(["target", "koreksi"], loc ="lower right")
axis_ud.title.set_text("Grafik Vertikal")

# Set the axis limits
axis_rl.set_xlim(0, 10)
axis_rl.set_ylim(-320, 320)

axis_ud.set_xlim(0, 10)
axis_ud.set_ylim(-320, 320)

# Define the update function
def update_rl(frame):
    target_rl.set_data(x_rl, y_target_rl)
    error_rl.set_data(x_rl, y_error_rl)

def update_ud(frame):
    target_ud.set_data(x_ud, y_target_ud)
    error_ud.set_data(x_ud, y_error_ud)


# Create a canvas to display the figure in Tkinter
canvas_rl = FigureCanvasTkAgg(fig_rl, master=win)
canvas_rl.get_tk_widget().place(x=930, y=180)

canvas_ud = FigureCanvasTkAgg(fig_ud, master=win)
canvas_ud.get_tk_widget().place(x=930, y=340)

# Create an animation object
rl = FuncAnimation(fig_rl, update_rl, interval=1)
ud = FuncAnimation(fig_ud, update_ud, interval=1)


win.mainloop()