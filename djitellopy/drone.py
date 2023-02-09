from . import Tello
import numpy as np
import cv2

class Drone:

	myDrone = Tello()
	integral = 0

	def __init__(self):
		self.send_rc_control = False
		self.myDrone.for_back_velocity = 0
		self.myDrone.left_right_velocity = 0
		self.myDrone.up_down_velocity = 0
		self.myDrone.yaw_velocity = 0
		self.myDrone.speed = 0
		self.myDrone.connect()
		self.myDrone.streamoff()
		self.myDrone.streamon()
		self.frame = self.myDrone.get_frame_read()
		print("Battery > ",self.myDrone.get_battery())

	def get_frame(self, w, h):
		frame = self.frame.frame
		frame = cv2.flip(frame, 1)
		frame = cv2.resize(frame, (w, h))
		return frame

	def get_drone(self):
		return self.myDrone
	
	def takeoff(self):
		self.myDrone.takeoff()
		self.send_rc_control = True

	def landing(self):
		self.myDrone.land()
		self.send_rc_control = False
	
	def clear(self):
		self.myDrone.send_rc_control(0, 0, 0, 0)

	def control(self, rl, fb, ud, yaw):
		self.myDrone.send_rc_control(rl, fb, ud, yaw)
