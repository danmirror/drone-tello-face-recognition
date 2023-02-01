from djitellopy import Face_Recognition
from djitellopy import Drone
from tkinter import *
import tkinter as tk
from tkinter import ttk
import pathlib
from PIL import ImageTk, Image

#Tello
import cv2

myDrone = Drone()
face_rec = Face_Recognition()

w, h = 640, 480
pid = [0.4, 0.4, 0]
pError = 0


win = Tk()
win.geometry("790x485")
win.title("Face Tracking & Recognition")
win.resizable(0,0)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer3.yml')

cascadePath = pathlib.Path(cv2.__file__).parent.absolute()/"data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(str(cascadePath))

font = cv2.FONT_HERSHEY_SIMPLEX
id = 0
jalan = False


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




def Tracking():
	def show_frames():
		status = 1
		if status == 1:
			# arduino = serial.Serial(port_list[port],baut_list[baut])
			frame = face_rec.get_frame( w, h)
			frame, status = face_rec.find_face(frame, faceCascade, comb_index, recognizer)
			if(not status):
				pass

			img = Image.fromarray(frame)
			imgtk = ImageTk.PhotoImage(image=img)
			label.imgtk = imgtk
			label.configure(image=imgtk, background="#FFFFFF")
			label.after(10, show_frames)
		else:
			print("Pilih Port dan Baut rate")
			label.after(10, show_frames)

	show_frames()

# Button for Tracking
tracking_button = Button(win, text="Tracking", height=1, width=10,
                          bg='#F2B830',
                          fg='#163e6c',
                          font=('helvetica', 12, 'bold'),
                          border=0, command=Tracking)
tracking_button.place(x=660, y=400)


def Close():
    win.destroy()
# Button for closing
exit_button = Button(win, text="Exit", height=1, width=10,
                          bg='#F2B830',
                          fg='#163e6c',
                          font=('helvetica', 12, 'bold'),
                          border=0, command=Close)
exit_button.place(x=660, y=435)

win.mainloop()