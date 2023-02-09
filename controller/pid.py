'''
	Proportional Integral Derivative 
	Danu andrean 
	2023

'''


import numpy as np

class PID:
	def __init__(self):
		self.speed = 0
		self.kp = 0
		self.ki = 0
		self.kd = 0
		self.previous_error = 0
		self.integral = 0

	def set(self, kp, ki, kd, speed):
		self.speed = speed
		self.kp = kp
		self.ki = ki
		self.kd = kd

	def clear(self):
		self.previous_error = 0
		self.integral = 0

	def update(self, current_error):
		self.integral += current_error 
		derivative = current_error - self.previous_error

		# PID EQUATION
		output = self.kp * current_error + self.ki * self.integral + self.kd * derivative
		self.previous_error = current_error

		output = int(np.clip(output, self.speed[0], self.speed[1]))
		return output

	