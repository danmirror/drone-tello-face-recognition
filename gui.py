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


w, h = 640, 480

is_drone = False

pid_ud = PID()
pid_rl = PID()

fuzzy_ud = Fuzzy()
fuzzy_rl = Fuzzy()

if is_drone :
    myDrone = Drone()

face_rec = Face_Recognition()


# data
x_rl = np.linspace(0,10,50)
y_target_rl = np.zeros(len(x_rl))
y_error_rl = np.zeros(len(x_rl))

x_ud = np.linspace(0,10,50)
y_target_ud = np.zeros(len(x_ud))
y_error_ud = np.zeros(len(x_ud))

x_speed = np.linspace(0,10,50)
y_target_speed = np.zeros(len(x_speed))
y_error_speed = np.zeros(len(x_ud))

def set_value():
    speed_ud = [int(ud_input1.get()), int(ud_input2.get())]
    speed_rl = [int(rl_input1.get()), int(rl_input2.get())]

    arr_min = [int(negative_input1.get()), int(negative_input2.get()), int(negative_input3.get())]
    arr_nor = [int(normal_input1.get()), int(normal_input2.get()), int(normal_input3.get())]
    arr_max = [int(positive_input1.get()), int(positive_input2.get()), int(positive_input3.get())]

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

    rl_input1["state"] = "disabled"
    ud_input1["state"] = "disabled"
    rl_input2["state"] = "disabled"
    ud_input2["state"] = "disabled"
    comb_face["state"] = "disabled"

def Takeoff():

    print("Takeoff")
    takeoff_button["state"] = "disabled"
    if is_drone :
        myDrone.takeoff()

def Landing():
    pass

def Close():
    print("closed")
    
    if is_drone :
        myDrone.landing()
    
    win.destroy()

def Tracking():
    
    global y_target_rl, y_error_rl, y_target_ud, y_error_ud

    set_value()
    disable()
    if is_drone :
        frame = myDrone.get_frame( w, h)
        battery_value.set(str(myDrone.get_battery()) +"%")
    else:
        frame = face_rec.get_frame( w, h)

    frame , info = face_rec.find_face_all(frame)
    # frame, info = face_rec.find_face(frame, comb_face, selectedX, selectedY)

    #right left 
    if info[0][0] != 0:

        error_rl =  w // 2 -info[0][0] 
       
        out_rl = fuzzy_rl.update(error_rl)
        print(" Output fuzzy rl ", out_rl)

        if is_drone :
            myDrone.control(0, 0, 0, out_rl)
        
        y_target_rl = np.append(y_target_rl, 0)
        y_target_rl = np.delete(y_target_rl, 0)
        y_error_rl = np.append(y_error_rl, error_rl)
        y_error_rl = np.delete(y_error_rl, 0)

    else:
        pid_rl.clear()
        fuzzy_rl.clear()

        if is_drone :
            myDrone.clear()
    
     #top down
    if info[0][1] != 0:
        error_ud =  h // 2 -info[0][1] 
       
        out_ud = fuzzy_ud.update(error_ud)
        print(" Output fuzzy ud ", out_ud)
    
        if is_drone :
            myDrone.control(0, 0, out_ud, 0)
        
        y_target_ud = np.append(y_target_ud, 0)
        y_target_ud = np.delete(y_target_ud, 0)
        y_error_ud = np.append(y_error_ud, error_ud)
        y_error_ud = np.delete(y_error_ud, 0)

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
win.geometry("1200x700")
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
frame_title =Frame(height = 150,width = 680,bg = "#FFFFFF")
frame_title.place(x= 0, y= 0)

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
                     fg="#aaaaaa", font="Helvetica 14 bold", width=50, height=5, anchor=CENTER)
label_title.place(x= 150, y= 0)

############################### Description ###############################
frame_des =Frame(height = 150,width = 500,bg = "#FFFFFF")
frame_des.place(x= 685, y= 0)
label_des = Label(frame_des, text="IMPLEMENTASI KENDALI PID PADA\n",
                     fg="#aaaaaa", font="Helvetica 14 bold", width=40, height=5, anchor=CENTER)
label_des.place(x= 0, y= 0)

############################### Image   ###############################
frame_container_img =Frame(height = h,width = w, bg = "#FFFFFF")
frame_container_img.place(x= 278, y= 160)

frame_image =Frame(height = h,width = w, bg = "#FFFFFF")
frame_image.place(x= 280, y= 160)

label =Label(frame_image)
label.grid(row=0, column=0)


############################### Face    ###############################
frame_face =Frame(height = 50,width = 120,bg = "#FFFFFF", padx=5, pady=5)
frame_face.place(x= 10, y= 160)

label_face = ttk.Label(frame_face, text="Face Selection", font='Helvetica 12 bold', background="#FFFFFF", foreground="#aaaaaa")
label_face.place(x=0 , y=0)

comb_face = ttk.Combobox(frame_face,textvariable=selected, values=["Dian","Yossi","Fahmizal","Alim","Matthew"], state="readonly", width=10)
comb_face.current(0)
comb_face.place (x=0 , y=20)

############################### Face Coordinate   ###############################
frame_coor =Frame(height = 110,width = 140,bg = "#FFFFFF", padx=5, pady=5)
frame_coor.place(x= 10, y= 230)
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


############################### Fuzzy   ###############################
frame_fuzzy =Frame(height = 100,width = 170,bg = "#FFFFFF")
frame_fuzzy.place(x= 10, y= 370)

label_fuzzy = ttk.Label(frame_fuzzy, text="Fuzzy", font='Helvetica 14 bold', foreground="#aaaaaa")
label_fuzzy.place(x=0 , y=0)
label_kp = ttk.Label(frame_fuzzy, text="Negatif")
label_kp.place(x=0 , y=30)
label_ki = ttk.Label(frame_fuzzy, text="Normal")
label_ki.place(x=0 , y=50)
label_kd = ttk.Label(frame_fuzzy, text="Positif")
label_kd.place(x=0 , y=70)

negative_input1 = tk.Entry(frame_fuzzy)
negative_input1.place(x=50, y=30, width=40)
negative_input1.insert(0, -200)
negative_input2 = tk.Entry(frame_fuzzy)
negative_input2.place(x=90, y=30, width=40)
negative_input2.insert(0, -150)
negative_input3 = tk.Entry(frame_fuzzy)
negative_input3.place(x=130, y=30, width=40)
negative_input3.insert(0, 0)

normal_input1 = tk.Entry(frame_fuzzy)
normal_input1.place(x=50, y=50, width=40)
normal_input1.insert(0, -150)
normal_input2 = tk.Entry(frame_fuzzy)
normal_input2.place(x=90, y=50, width=40)
normal_input2.insert(0, 0)
normal_input3 = tk.Entry(frame_fuzzy)
normal_input3.place(x=130, y=50, width=40)
normal_input3.insert(0, 150)

positive_input1 = tk.Entry(frame_fuzzy)
positive_input1.place(x=50, y=70, width=40)
positive_input1.insert(0, 0)
positive_input2 = tk.Entry(frame_fuzzy)
positive_input2.place(x=90, y=70, width=40)
positive_input2.insert(0, 150)
positive_input3 = tk.Entry(frame_fuzzy)
positive_input3.place(x=130, y=70, width=40)
positive_input3.insert(0, 200)


############################### Speed   ###############################
frame_speed =Frame(height = 70,width = 120,bg = "#FFFFFF", padx=5, pady=5)
frame_speed.place(x= 10, y= 490)

label_speed = ttk.Label(frame_speed, text="Speed", font='Helvetica 14 bold', background="#FFFFFF", foreground="#aaaaaa")
label_speed.place(x=0 , y=0)
label_rl = ttk.Label(frame_speed, text="RL")
label_rl.place(x=0 , y=20)
label_ud = ttk.Label(frame_speed, text="UD")
label_ud.place(x=0 , y=40)

rl_input1 = tk.Entry(frame_speed)
rl_input1.place(x=30, y=20, width=40)
rl_input1.insert(0, -50)
rl_input2 = tk.Entry(frame_speed)
rl_input2.place(x=70, y=20, width=40)
rl_input2.insert(0, 50)

ud_input1 = tk.Entry(frame_speed)
ud_input1.place(x=30, y=40, width=40)
ud_input1.insert(0, -50)
ud_input2 = tk.Entry(frame_speed)
ud_input2.place(x=70, y=40, width=40)
ud_input2.insert(0, 50)

############################### Battery ###############################
frame_bat =Frame(height = 40,width = 130,bg = "#FFFFFF", padx=5, pady=5)
frame_bat.place(x= 10, y= 590)
label_bat = ttk.Label(frame_bat, text="Battery", font='Helvetica 12 bold', background="#FFFFFF", foreground="#aaaaaa")
label_bat.place(x=0 , y=0)

battery = Entry(frame_bat,width=8, font=('Arial', 14),textvariable=battery_value)
battery.place(x=60, y=0, width=40)


# Button for Tracking
tracking_button = Button(win, text="Tracking", height=1, width=10,bg='#F2B830',fg='#163e6c',font=('helvetica', 12, 'bold'), border=0, command=Tracking)
tracking_button.place(x=280, y=650)

takeoff_button = Button(win, text="TakeOff", height=1, width=10, bg='#F2B830', fg='#163e6c', font=('helvetica', 12, 'bold'), border=0, command=Takeoff)
takeoff_button.place(x=450, y=650)

landing_button = Button(win, text="Landing", height=1, width=10, bg='#F2B830', fg='#163e6c', font=('helvetica', 12, 'bold'), border=0, command=Landing)
landing_button.place(x=640, y=650)

# Button for closing
exit_button = Button(win, text="Exit", height=1, width=10,  bg='#F2B830', fg='#163e6c', font=('helvetica', 12, 'bold'), border=0, command=Close)
exit_button.place(x=800, y=650)


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

fig_speed = plt.Figure(figsize=(3.5, 2), dpi=70)
axis_speed = fig_speed.add_subplot(1, 1, 1)
target_speed, = axis_speed.plot(x_speed, y_target_speed, color='blue', label='target 1')
error_speed, = axis_speed.plot(x_speed, y_error_speed, color='red', label='error 1')
axis_speed.legend(["target", "koreksi"], loc ="lower right")
axis_speed.title.set_text("Grafik Vertikal")


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

def update_speed(frame):
    target_ud.set_data(x_ud, y_target_ud)
    error_ud.set_data(x_ud, y_error_ud)



# Create a canvas to display the figure in Tkinter
canvas_rl = FigureCanvasTkAgg(fig_rl, master=win)
canvas_rl.get_tk_widget().place(x=925, y=180)

canvas_ud = FigureCanvasTkAgg(fig_ud, master=win)
canvas_ud.get_tk_widget().place(x=925, y=340)

canvas_speed = FigureCanvasTkAgg(fig_speed, master=win)
canvas_speed.get_tk_widget().place(x=925, y=500)

# Create an animation object
rl = FuncAnimation(fig_rl, update_rl, interval=1)
ud = FuncAnimation(fig_ud, update_ud, interval=1)


win.mainloop()