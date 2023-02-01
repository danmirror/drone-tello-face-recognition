from djitellopy import Tello
from djitellopy import Drone

from tkinter import *
import tkinter as tk
from tkinter import ttk
import pathlib
from PIL import ImageTk, Image

import cv2

# Drone initial
myDrone = Drone()


# GUI initial
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

names = ['None', 'Dian', 'Yossi',"Fahmizal","Alim", "Matthew"]
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


def Tracking():
	def show_frames():
		status = 1
		if status == 1:
			# arduino = serial.Serial(port_list[port],baut_list[baut])
			# ret, frame = cap.read()
			frame = myDrone.get_frame()

			# frame = cv2.flip(frame, 1)
			frame = cv2.resize(frame, (640, 480))
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			faces = faceCascade.detectMultiScale(
				gray,
				scaleFactor=1.35,
				minNeighbors=5,
				minSize=(60, 60))
			index = comb_index.current()
			for (x, y, w, h) in faces:
				id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

				if (confidence < 70):  # filter presentase confidence yang terdeteksi
					id = names[id]
					confidence = "  {0}%".format(round(100 - confidence))  # presentase confidence yang terdeteksi
				else:
					id = "unknown"
					confidence = 0

				x_pos = x + (w / 2)
				y_pos = y + (h / 2)

				x1_pos = x_pos
				x1_pos = int(x1_pos)
				y1_pos = y_pos
				y1_pos = int(y1_pos)

				if x_pos >= 310 and x_pos <= 330:
					x_pos = 320
				if y_pos >= 225 and y_pos <= 255:
					y_pos = 240

				x_pos = x_pos / 640 * 180
				y_pos = y_pos / 480 * 180
				x_pos = int(x_pos)
				y_pos = int(y_pos)
				x1_text = str(x1_pos)
				y1_text = str(y1_pos)

				if id == names[1] and index == 0:  # Alim
					cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
					cv2.putText(frame, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
					cv2.putText(frame, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
					selectedX.set(x1_text)
					selectedY.set(y1_text)
					string = 'X{0:d}Y{1:d}'.format(x_pos, y_pos)
					# arduino.write(string.encode('utf-8',errors="ignore"))

				if id == names[2] and index == 1:  # Matthew
					cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
					cv2.putText(frame, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
					cv2.putText(frame, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
					selectedX.set(x1_text)
					selectedY.set(y1_text)
					string = 'X{0:d}Y{1:d}'.format(x_pos, y_pos)
					# arduino.write(string.encode('utf-8',errors="ignore"))

				if id == names[3] and index == 2:  # Dian
					cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
					cv2.putText(frame, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
					cv2.putText(frame, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
					selectedX.set(x1_text)
					selectedY.set(y1_text)
					string = 'X{0:d}Y{1:d}'.format(x_pos, y_pos)
					# arduino.write(string.encode('utf-8',errors="ignore"))

				if id == names[4] and index == 3:  # Yossi
					cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
					cv2.putText(frame, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
					cv2.putText(frame, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
					selectedX.set(x1_text)
					selectedY.set(y1_text)
					string = 'X{0:d}Y{1:d}'.format(x_pos, y_pos)
					# arduino.write(string.encode('utf-8',errors="ignore"))

				if id == names[5] and index == 4:  # Fahmizal
					cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
					cv2.putText(frame, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
					cv2.putText(frame, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
					selectedX.set(x1_text)
					selectedY.set(y1_text)
					string = 'X{0:d}Y{1:d}'.format(x_pos, y_pos)
					# arduino.write(string.encode('utf-8',errors="ignore"))

				else:
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

def Close():
    win.destroy()

# Button for Tracking
tracking_button = Button(win, text="Tracking", height=1, width=10,
                          bg='#F2B830',
                          fg='#163e6c',
                          font=('helvetica', 12, 'bold'),
                          border=0, command=Tracking)
tracking_button.place(x=660, y=400)

# Button for closing
exit_button = Button(win, text="Exit", height=1, width=10,
                          bg='#F2B830',
                          fg='#163e6c',
                          font=('helvetica', 12, 'bold'),
                          border=0, command=Close)
exit_button.place(x=660, y=435)

win.mainloop()