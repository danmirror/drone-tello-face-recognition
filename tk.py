from tkinter import *   
from tkinter import ttk
win = Tk()
win.geometry("1200x680")
fm =Frame(height = 100,width = 640,bg = "#FFFFFF")
fm.place(x= 150, y= 0)

label_PID = ttk.Label(fm, text="PID", font='Helvetica 14 bold', foreground="#aaaaaa")
label_PID.place(x=0 , y=10)
win.mainloop() 