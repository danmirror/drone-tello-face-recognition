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
mode = False

fuzzy_ud = Fuzzy()
fuzzy_rl = Fuzzy()

if is_drone :
    myDrone = Drone()

face_rec = Face_Recognition()


w, h = 640, 480
# data
x_rl = np.linspace(0,10,50)
y_target_rl = np.zeros(len(x_rl))
y_error_rl = np.zeros(len(x_rl))
y_average_rl = np.zeros(len(x_rl))

x_ud = np.linspace(0,10,50)
y_target_ud = np.zeros(len(x_ud))
y_error_ud = np.zeros(len(x_ud))
y_average_ud = np.zeros(len(x_ud))

x_speed = np.linspace(0,10,50)
y_target_speed = np.zeros(len(x_speed))
y_error_speed_ud = np.zeros(len(x_speed))
y_error_speed_rl = np.zeros(len(x_speed))

def set_value():
    speed_ud = [int(ud_input1.get()), int(ud_input2.get())]
    speed_rl = [int(rl_input1.get()), int(rl_input2.get())]

    arr_min = [int(negative_input1.get()), int(negative_input2.get()), int(negative_input3.get())]
    arr_nor = [int(normal_input1.get()), int(normal_input2.get()), int(normal_input3.get())]
    arr_max = [int(positive_input1.get()), int(positive_input2.get()), int(positive_input3.get())]

    fuzzy_ud.set(arr_min, arr_nor, arr_max, speed_ud)
    fuzzy_rl.set(arr_min, arr_nor, arr_max, speed_rl)

def disable():
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
    comb_mode["state"] = "disabled"

def enable():
    negative_input1["state"] = "normal"
    negative_input2["state"] = "normal"
    negative_input3["state"] = "normal"

    normal_input1["state"] = "normal"
    normal_input2["state"] = "normal"
    normal_input3["state"] = "normal"

    positive_input1["state"] = "normal"
    positive_input2["state"] = "normal"
    positive_input3["state"] = "normal"

    rl_input1["state"] = "normal"
    ud_input1["state"] = "normal"
    rl_input2["state"] = "normal"
    ud_input2["state"] = "normal"
    comb_face["state"] = "normal"
    comb_mode["state"] = "normal"

def Takeoff():
    global state_running, mode
    if not state_running: 
        print("Takeoff")
        
        if is_drone :
            myDrone.takeoff()

        landing_button["state"] = "normal"
        takeoff_button["state"] = "disabled"
        tracking_button["state"] = "normal"
        
        if(selected_mode.get() == "Realtime"):
            print("using realtime mode")
            mode = True
        if selected_mode.get() == "Fuzzy":
            print("using fuzzy scale mode")
            mode = False
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
    
    global  y_error_rl, y_average_rl, y_error_ud, y_average_ud, y_error_speed_rl, y_error_speed_ud,state_running, mode
    
    if(state_running):
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
        
            out_rl, ret_err_rl, ret_average_rl, ret_speed_rl = fuzzy_rl.update(error_rl, mode)
            # print(" Output fuzzy rl ", error_rl)
            # print(" Output fuzzy ret rl ", ret_err_rl)

            if is_drone :
                myDrone.control(0, 0, 0, out_rl)
            
            y_error_rl = np.append(y_error_rl, ret_err_rl)
            y_error_rl = np.delete(y_error_rl, 0)
            y_average_rl = np.append(y_average_rl, ret_average_rl)
            y_average_rl = np.delete(y_average_rl, 0)
            y_error_speed_rl = np.append(y_error_speed_rl, ret_speed_rl)
            y_error_speed_rl = np.delete(y_error_speed_rl, 0)

        else:
            # fuzzy_rl.clear()

            if is_drone :
                myDrone.clear()
        
        # #top down
        # if info[0][1] != 0:
        #     error_ud =  h // 2 -info[0][1] 
        
        #     out_ud, ret_err_ud, ret_average_ud, ret_speed_ud  = fuzzy_ud.update(error_ud, mode)
        #     # print(" Output fuzzy ud ", error_ud)
        #     # print(" Output fuzzy ret ud ", ret_err_ud)
        
        #     if is_drone :
        #         myDrone.control(0, 0, out_ud, 0)
            
        #     y_error_ud = np.append(y_error_ud, ret_err_ud)
        #     y_error_ud = np.delete(y_error_ud, 0)
        #     y_average_ud = np.append(y_average_ud, ret_average_ud)
        #     y_average_ud = np.delete(y_average_ud, 0)
        #     y_error_speed_ud = np.append(y_error_speed_ud, ret_speed_ud)
        #     y_error_speed_ud = np.delete(y_error_speed_ud, 0)

        # else:
        #     # fuzzy_ud.clear()

        #     if is_drone :
        #         myDrone.clear()

        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk, background="#FFFFFF")
        label.after(1, Tracking)



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
selected_mode = tk.StringVar()

############################### Title ###############################
frame_title =Frame(height = 150,width = 680,bg = "#FFFFFF", padx=30, pady=30)
frame_title.place(x= 0, y= 0)

logo = Image.open("ui_data/ugm.png")
logo_resize = logo.resize((120,100))
img = ImageTk.PhotoImage(logo_resize)
logoo = Label(frame_title, image=img,background ="#FFFFFF")
logoo.image = img
logoo.place(x= 0, y= 0)
label_title = Label(frame_title, text="Implementasi Kendali Fuzzy Logic Untuk Stabilisasi\n"
                    "Pelacakan Pada Sistem Pengenalan Wajah Manusia Dengan\n"
                    "Metode LBPH Face Recognition Pada Quadcopter Drone",
                     fg="#aaaaaa", bg = "#FFFFFF", font="Helvetica 12 bold", width=50, height=5, anchor=CENTER)
label_title.place(x= 150, y= 0)

############################### Description ###############################
frame_des =Frame(height = 150,width = 520,bg = "#FFFFFF", padx=30, pady=30)
frame_des.place(x= 685, y= 0)
label_des = Label(frame_des, text="Oleh:\n"
                    "Nama : Dian Lestari Puteri\n"
                    "NIM : 21/483637/SV/20402\n"
                    "Prodi : Teknologi Rekayasa Instrumentasi dan Kontrol",
                     fg="#aaaaaa",bg = "#FFFFFF", font="Helvetica 12", width=60, height=5, anchor=NW, justify="left")
label_des.place(x= 0, y= 0)


############################### Image   ###############################
frame_container_img =Frame(height = h,width = w, bg = "#FFFFFF")
frame_container_img.place(x= 268, y= 160)

frame_image =Frame(height = h,width = w, bg = "#FFFFFF")
frame_image.place(x= 270, y= 160)

label =Label(frame_image)
label.grid(row=0, column=0)


############################### Face    ###############################
frame_face =Frame(height = 50,width = 230,bg = "#FFFFFF", padx=5, pady=5)
frame_face.place(x= 20, y= 160)

label_face = ttk.Label(frame_face, text="Face Selection", font='Helvetica 12 bold', background="#FFFFFF", foreground="#aaaaaa")
label_face.place(x=0 , y=0)

comb_face = ttk.Combobox(frame_face,textvariable=selected, values=["Dian","Yossi","Fahmizal","Alim","Matthew"], state="readonly", width=25)
comb_face.current(0)
comb_face.place (x=0 , y=20)

############################### Face Coordinate   ###############################
frame_coor =Frame(height = 110,width = 230,bg = "#FFFFFF", padx=5, pady=5)
frame_coor.place(x= 20, y= 230)
label_coor = ttk.Label(frame_coor, text="Face Coordinate", background ="#FFFFFF", font='Helvetica 12 bold', foreground="#aaaaaa")
label_coor.place(x=0 , y=0)

label_x = ttk.Label(frame_coor, text="X =", background ="#FFFFFF")
label_x.place(x=0 , y=30)

label_y = ttk.Label(frame_coor, text="Y =", background ="#FFFFFF")
label_y.place(x=0 , y=65)

x_dis = Entry(frame_coor, width=12, font=('Arial', 14), textvariable=selectedX)
x_dis.place(x=30, y=30)

y_dis = Entry( frame_coor, width=12, font=('Arial', 14),textvariable=selectedY)
y_dis.place(x=30, y=65)


############################### Fuzzy   ###############################
frame_fuzzy =Frame(height = 110,width = 230,bg = "#FFFFFF", padx=5, pady=5)
frame_fuzzy.place(x= 20, y= 360)

label_fuzzy = ttk.Label(frame_fuzzy, text="Fuzzy", font='Helvetica 12 bold', foreground="#aaaaaa", background ="#FFFFFF")
label_fuzzy.place(x=0 , y=0)
label_kp = ttk.Label(frame_fuzzy, text="Negatif", background ="#FFFFFF")
label_kp.place(x=0 , y=30)
label_ki = ttk.Label(frame_fuzzy, text="Normal", background ="#FFFFFF")
label_ki.place(x=0 , y=50)
label_kd = ttk.Label(frame_fuzzy, text="Positif", background ="#FFFFFF")
label_kd.place(x=0 , y=70)

negative_input1 = tk.Entry(frame_fuzzy)
negative_input1.place(x=70, y=30, width=50)
negative_input1.insert(0, -200)
negative_input2 = tk.Entry(frame_fuzzy)
negative_input2.place(x=120, y=30, width=50)
negative_input2.insert(0, -150)
negative_input3 = tk.Entry(frame_fuzzy)
negative_input3.place(x=170, y=30, width=50)
negative_input3.insert(0, 0)

normal_input1 = tk.Entry(frame_fuzzy)
normal_input1.place(x=70, y=50, width=50)
normal_input1.insert(0, -150)
normal_input2 = tk.Entry(frame_fuzzy)
normal_input2.place(x=120, y=50, width=50)
normal_input2.insert(0, 0)
normal_input3 = tk.Entry(frame_fuzzy)
normal_input3.place(x=170, y=50, width=50)
normal_input3.insert(0, 150)

positive_input1 = tk.Entry(frame_fuzzy)
positive_input1.place(x=70, y=70, width=50)
positive_input1.insert(0, 0)
positive_input2 = tk.Entry(frame_fuzzy)
positive_input2.place(x=120, y=70, width=50)
positive_input2.insert(0, 150)
positive_input3 = tk.Entry(frame_fuzzy)
positive_input3.place(x=170, y=70, width=50)
positive_input3.insert(0, 200)


############################### Speed   ###############################
frame_speed =Frame(height = 80,width = 230,bg = "#FFFFFF", padx=5, pady=5)
frame_speed.place(x= 20, y= 490)

label_speed = ttk.Label(frame_speed, text="Speed", font='Helvetica 12 bold', background="#FFFFFF", foreground="#aaaaaa")
label_speed.place(x=0 , y=0)
label_rl = ttk.Label(frame_speed, text="RL", background ="#FFFFFF")
label_rl.place(x=0 , y=20)
label_ud = ttk.Label(frame_speed, text="UD", background ="#FFFFFF")
label_ud.place(x=0 , y=40)

rl_input1 = tk.Entry(frame_speed)
rl_input1.place(x=70, y=20, width=70)
rl_input1.insert(0, -50)
rl_input2 = tk.Entry(frame_speed)
rl_input2.place(x=140, y=20, width=70)
rl_input2.insert(0, 50)

ud_input1 = tk.Entry(frame_speed)
ud_input1.place(x=70, y=40, width=70)
ud_input1.insert(0, -50)
ud_input2 = tk.Entry(frame_speed)
ud_input2.place(x=140, y=40, width=70)
ud_input2.insert(0, 50)

############################### Battery ###############################
frame_bat =Frame(height = 40,width = 230,bg = "#FFFFFF", padx=5, pady=5)
frame_bat.place(x= 20, y= 590)
label_bat = ttk.Label(frame_bat, text="Battery", font='Helvetica 12 bold', background="#FFFFFF", foreground="#aaaaaa")
label_bat.place(x=0 , y=0)

battery = Entry(frame_bat,width=8, font=('Arial', 14),textvariable=battery_value)
battery.place(x=70, y=0, width=120)

############################## select mode ###########################
frame_mode =Frame(height = 40,width = 230,bg = "#FFFFFF", padx=5, pady=5)
frame_mode.place(x= 20, y=650)
label_mode = ttk.Label(frame_mode, text="Mode", font='Helvetica 12 bold', background="#FFFFFF", foreground="#aaaaaa")
label_mode.place(x=0 , y=0)
comb_mode = ttk.Combobox(frame_mode,textvariable=selected_mode, values=["Realtime","Fuzzy"], state="readonly", width=15)
comb_mode.current(0)
comb_mode.place (x=70 , y=0)

# Button for Tracking
tracking_button = Button(win, text="Tracking", state="disabled", height=1, width=10,bg='#F2B830',fg='#163e6c',font=('helvetica', 12, 'bold'), border=0, command=Tracking)
tracking_button.place(x=270, y=650)

takeoff_button = Button(win, text="TakeOff", height=1, width=10, bg='#F2B830', fg='#163e6c', font=('helvetica', 12, 'bold'), border=0, command=Takeoff)
takeoff_button.place(x=440, y=650)

landing_button = Button(win, text="Landing", state="disabled", height=1, width=10, bg='#F2B830', fg='#163e6c', font=('helvetica', 12, 'bold'), border=0, command=Landing)
landing_button.place(x=630, y=650)

# Button for closing
exit_button = Button(win, text="Exit", height=1, width=10,  bg='#F2B830', fg='#163e6c', font=('helvetica', 12, 'bold'), border=0, command=Close)
exit_button.place(x=790, y=650)


fig_rl = plt.Figure(figsize=(3.5, 2), dpi=70)
axis_rl = fig_rl.add_subplot(1, 1, 1)
target_rl, = axis_rl.plot(x_rl, y_target_rl, color='blue', label='target 1')
error_rl, = axis_rl.plot(x_rl, y_error_rl, color='red', label='error 1')
average_rl, = axis_rl.plot(x_rl, y_average_rl, color='yellow', label='error 2')
axis_rl.legend(["T","E","A"], loc ="lower right")
axis_rl.title.set_text("Grafik Yaw")

fig_ud = plt.Figure(figsize=(3.5, 2), dpi=70)
axis_ud = fig_ud.add_subplot(1, 1, 1)
target_ud, = axis_ud.plot(x_ud, y_target_ud, color='blue', label='target 1')
error_ud, = axis_ud.plot(x_ud, y_error_ud, color='red', label='error 1')
average_ud, = axis_ud.plot(x_ud, y_average_ud, color='yellow', label='error 2')
axis_ud.legend(["T","E","A"], loc ="lower right")
axis_ud.title.set_text("Grafik Vertikal")

fig_speed = plt.Figure(figsize=(3.5, 2), dpi=70)
axis_speed = fig_speed.add_subplot(1, 1, 1)
target_speed, = axis_speed.plot(x_speed, y_target_speed, color='blue', label='target 1')
error_speed_rl, = axis_speed.plot(x_speed, y_error_speed_rl, color='red', label='error 1')
error_speed_ud, = axis_speed.plot(x_speed, y_error_speed_ud, color='yellow', label='error 2')
axis_speed.legend(["T","RL","UD"], loc ="lower right")
axis_speed.title.set_text("Grafik Speed")


# Set the axis limits
axis_rl.set_xlim(0, 10)
axis_rl.set_ylim(-320, 320)

axis_ud.set_xlim(0, 10)
axis_ud.set_ylim(-320, 320)

axis_speed.set_xlim(0, 10)
axis_speed.set_ylim(-50, 50)

# Define the update function
def update_rl(frame):
    error_rl.set_data(x_rl, y_error_rl)
    average_rl.set_data(x_rl, y_average_rl)
    return error_rl, average_rl

def update_ud(frame):
    error_ud.set_data(x_ud, y_error_ud)
    average_ud.set_data(x_rl, y_average_ud)
    return error_ud, average_ud

def update_speed(frame):
    error_speed_rl.set_data(x_speed, y_error_speed_rl)
    error_speed_ud.set_data(x_speed, y_error_speed_ud)
    return error_speed_rl, error_speed_ud

# Create a canvas to display the figure in Tkinter
canvas_rl = FigureCanvasTkAgg(fig_rl, master=win)
canvas_rl.get_tk_widget().place(x=930, y=160)

canvas_ud = FigureCanvasTkAgg(fig_ud, master=win)
canvas_ud.get_tk_widget().place(x=930, y=325)

canvas_speed = FigureCanvasTkAgg(fig_speed, master=win)
canvas_speed.get_tk_widget().place(x=930, y=500)

# Create an animation object
e = FuncAnimation(fig_rl, update_rl, interval=0, blit=True)
a = FuncAnimation(fig_ud, update_ud, interval=0, blit=True)
s = FuncAnimation(fig_speed, update_speed, interval=0, blit=True)


win.mainloop()