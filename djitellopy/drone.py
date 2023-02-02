from . import Tello
import numpy as np

class Drone:

	myDrone = Tello()

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

	def get_frame(self):
		return self.myDrone.get_frame_read().frame
	
	def get_drone(self):
		return self.myDrone
	
	def printf(self):
		print("halo drone")

	def tracking_face(self, info, w, pid, pError):
		## PID
		error = info[0][0] - w // 2
		speed = pid[0] * error + pid[1] * (error - pError)
		speed = int(np.clip(speed, -100, 100))

		print(speed)
		if info[0][0] != 0:
			self.myDrone.yaw_velocity = speed
		else:
			self.myDrone.for_back_velocity = 0
			self.myDrone.left_right_velocity = 0
			self.myDrone.up_down_velocity = 0
			self.myDrone.yaw_velocity = 0
			error = 0
		if self.myDrone.send_rc_control:
			self.myDrone.send_rc_control(self.myDrone.left_right_velocity,
									self.myDrone.for_back_velocity,
									self.myDrone.up_down_velocity,
									self.myDrone.yaw_velocity)
		return error