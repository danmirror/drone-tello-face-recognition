from . import Tello
import numpy as np
import cv2

class Drone:

	myDrone = Tello()
	
	integral = 0

	def __init__(self):
		
		self.myDrone.connect()
		self.myDrone.for_back_velocity = 0
		self.myDrone.left_right_velocity = 0
		self.myDrone.up_down_velocity = 0
		self.myDrone.yaw_velocity = 0
		self.myDrone.speed = 0
		print("Battery > ",self.myDrone.get_battery())
		self.myDrone.streamoff()
		self.myDrone.streamon()
		self.frame = self.myDrone.get_frame_read()

	def get_frame(self, w, h):
		frame = self.frame.frame
		frame = cv2.flip(frame, 1)
		frame = cv2.resize(frame, (w, h))
		return frame

	def get_drone(self):
		return self.myDrone
	
	def printf(self):
		print("halo drone")

	def tracking_face(self, info, w, pid, pError):
		## PID
		kp = pid[0]
		ki = pid[1]
		kd = pid[2]
		error = info[0][0] - w // 2

		if info[0][0] != 0:
		
			self.integral += error
			derivative = error - pError
			
			# PID EQUATION
			output = kp * error + ki * self.integral + kd * derivative
			# print("output", output)
			
			speed = int(np.clip(output, -100, 100))

		
			print("error", error)
			print("integral", self.integral)
			print(speed)
			self.myDrone.yaw_velocity = speed
		else:
			self.myDrone.for_back_velocity = 0
			self.myDrone.left_right_velocity = 0
			self.myDrone.up_down_velocity = 0
			self.myDrone.yaw_velocity = 0
			error = 0
			integral = 0

		if self.myDrone.send_rc_control:
			self.myDrone.send_rc_control(self.myDrone.left_right_velocity,
									self.myDrone.for_back_velocity,
									self.myDrone.up_down_velocity,
									self.myDrone.yaw_velocity)
		return error
	
	# fuzzy jauh sedang deket
	#
	# 
	#
	#