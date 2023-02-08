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

	def tracking_face(self, info, w, pid, pError):
		## PID
		kp = pid[0]
		ki = pid[1]
		kd = pid[2]
		error =  w // 2 -info[0][0] 
		
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

		if self.send_rc_control :
			self.myDrone.send_rc_control(self.myDrone.left_right_velocity,
									self.myDrone.for_back_velocity,
									self.myDrone.up_down_velocity,
									self.myDrone.yaw_velocity)
		return error
	
	def triangular_mf(self, x, a, b, c):
		if x <= a:
			return 0
		elif x > a and x < b:
			return (x - a) / (b - a)
		elif x >= b and x < c:
			return (c - x) / (c - b)
		else:
			return 0

	def fuzzy_logic_mamdani(self, info, w, pError):

		error =  w // 2 - info[0][1] 
		if info[0][1] != 0:
			derivative = (error + pError) //2  

			# Membership function for error
			error_low = self.triangular_mf(error, -200, -150, 0)
			error_medium = self.triangular_mf(error, -150, 0, 150)
			error_high = self.triangular_mf(error, 0, 150, 200)

			# Membership function for derivative
			derivative_negatif = self.triangular_mf(derivative, -200, -150, 0)
			derivative_nol = self.triangular_mf(derivative, -150, 0, 150)
			derivative_positif = self.triangular_mf(derivative, 0, 150, 200)

			# Rule base
			rule_base = [
				(min(error_low, derivative_negatif), 'fast'),
				(min(error_low, derivative_nol), 'normal'),
				(min(error_low, derivative_positif), 'slow'),
				(min(error_medium, derivative_negatif), 'fast'),
				(min(error_medium, derivative_nol), 'normal'),
				(min(error_medium, derivative_positif), 'normal'),
				(min(error_high, derivative_negatif), 'normal'),
				(min(error_high, derivative_nol), 'slow'),
				(min(error_high, derivative_positif), 'slow')
			]

			# Defuzzification
			defuzzified_value = 0
			total_weight = 0
			for r in rule_base:
				weight = r[0]
				if weight > 0:
					if r[1] == 'slow':
						defuzzified_value += weight * -20
						total_weight += weight
					elif r[1] == 'normal':
						defuzzified_value += weight * 0
						total_weight += weight
					elif r[1] == 'fast':
						defuzzified_value += weight * 20
						total_weight += weight
			speed = 0
			if not total_weight ==  0:
				speed = - defuzzified_value / total_weight
			print("fuzzy", speed)
			self.myDrone.up_down_velocity =int( speed)
		else:
			self.myDrone.for_back_velocity = 0
			self.myDrone.left_right_velocity = 0
			self.myDrone.up_down_velocity = 0
			self.myDrone.yaw_velocity = 0
			error = 0

		if self.send_rc_control :
			self.myDrone.send_rc_control(self.myDrone.left_right_velocity,
									self.myDrone.for_back_velocity,
									self.myDrone.up_down_velocity,
									self.myDrone.yaw_velocity)
		return int(error)

	