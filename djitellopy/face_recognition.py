from . import Tello
import pathlib
import cv2
import numpy as np
import time


class Face_Recognition:
	cap= cv2.VideoCapture(0)

	names = ['None', 'Dian', 'Yossi',"Fahmizal","Alim", "Matthew"]
	recognizer = cv2.face.LBPHFaceRecognizer_create()
	
	recognizer.read('trainer/trainer3.yml')

	cascadePath = pathlib.Path(cv2.__file__).parent.absolute()/"data/haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(str(cascadePath))

	font = cv2.FONT_HERSHEY_SIMPLEX
	
	integral = 0

	def __init__(self):
		print("Initial Face")


	def get_frame(self, w, h):
		ret, frame = self.cap.read()
		frame = cv2.flip(frame, 1)
		frame = cv2.resize(frame, (w, h))
		return frame
	
	def find_face_all(self, frame):
		faceCascade = cv2.CascadeClassifier('trainer/cascadeee.xml')
		imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(imgGray, 1.1, 6)

		myFaceListC = []
		myFaceListArea = []

		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
			cx = x + w // 2
			cy = y + h // 2
			area = w * h
			myFaceListArea.append(area)
			myFaceListC.append([cx, cy])

		if len(myFaceListArea) != 0:
			i = myFaceListArea.index(max(myFaceListArea))
			return frame, [myFaceListC[i], myFaceListArea[i]]
		else:
			return frame, [[0, 0], 0]

	def find_face(self, frame, comb_index, selectedX, selectedY):
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = self.faceCascade.detectMultiScale(
			gray,
			scaleFactor=1.35,
			minNeighbors=5,
			minSize=(60, 60))
		index = comb_index.current()

		myFaceListC = []
		myFaceListArea = []

		for (x, y, w, h) in faces:
			id, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])

			if (confidence < 70):  # filter presentase confidence yang terdeteksi
				id = self.names[id]
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

			id_1 = id == self.names[1] and index == 0
			id_2 = id == self.names[2] and index == 1
			id_3 = id == self.names[3] and index == 2
			id_4 = id == self.names[4] and index == 3
			id_5 = id == self.names[5] and index == 4

			if id_1 or id_2 or id_3 or id_4 or id_5 :
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				cv2.putText(frame, str(id), (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
				cv2.putText(frame, str(confidence), (x + 5, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1)
				
				# Insert value
				cx = x + w // 2
				cy = y + h // 2
				area = w * h
				myFaceListArea.append(area)
				myFaceListC.append([cx, cy])

				# Update UI
				selectedX.set(x1_text)
				selectedY.set(y1_text)
				string = 'X{0:d}Y{1:d}'.format(x_pos, y_pos)

			else:
				return frame, False,  [[0, 0], 0]

		if len(myFaceListArea) != 0:
			i = myFaceListArea.index(max(myFaceListArea))
			return frame, True, [myFaceListC[i], myFaceListArea[i]]
		else:
			return frame, True, [[0, 0], 0]

	def face_tracking(self, info, w, pid, pError):
		## PID
		kp = pid[0]
		ki = pid[1]
		kd = pid[2]
		error = info[0][0] - w // 2

		if info[0][0] != 0:
		
			self.integral += error
			# print("error", error)
			# print("integral", self.integral)
			derivative = error - pError
			# PID EQUATION
			output = kp * error + ki * self.integral + kd * derivative
			# print("output", output)
			
			speed = int(np.clip(output, -100, 100))

		
			print("PID ", speed)
		# 	self.myDrone.yaw_velocity = speed
		else:
			# self.myDrone.for_back_velocity = 0
			# self.myDrone.left_right_velocity = 0
			# self.myDrone.up_down_velocity = 0
			# self.myDrone.yaw_velocity = 0
			error = 0
			integral = 0
		# if self.myDrone.send_rc_control:
		# 	self.myDrone.send_rc_control(self.myDrone.left_right_velocity,
		# 							self.myDrone.for_back_velocity,
		# 							self.myDrone.up_down_velocity,
		# 							self.myDrone.yaw_velocity)
		return error

class Fuzzy:
	# Definisikan fungsi keanggotaan (membership function)
	membership_functions = [
		{
			# Fungsi keanggotaan error negatif besar (NB) dan delta error negatif besar (DB)
			'error': [-100, -50, 0],
			'd_error': [-100, -50, 0],
			'output': -100
		},
		{
			# Fungsi keanggotaan error negatif sedang (NS) dan delta error negatif sedang (DS)
			'error': [-50, 0, 50],
			'd_error': [-50, 0, 50],
			'output': 0
		},
		{
			# Fungsi keanggotaan error positif besar (PB) dan delta error positif besar (PB)
			'error': [0, 50, 100],
			'd_error': [0, 50, 100],
			'output': 100
		}
	]
	def __init__(self):
		print("Initial Fuzzy")

	def triangular(self, value, a, b, c):
		if value < a:
			return 0
		elif value >= a and value < b:
			return (value - a) / (b - a)
		elif value >= b and value <= c:
			return (c - value) / (c - b)
		else:
			return 0

	# fuzzyfikasi menggunakan logika fuzzy "and" (min) MAMDANI
	def fuzzyfikasi(self, error, d_error, membership_functions):
		outputs = []
		for mf in self.membership_functions:
			error_degree = self.triangular(error, mf['error'][0], mf['error'][1], mf['error'][2])
			d_error_degree = self.triangular(d_error, mf['d_error'][0], mf['d_error'][1], mf['d_error'][2])
			output_degree = min(error_degree, d_error_degree)
			outputs.append(output_degree * mf['output'])
		return outputs

	# defuzzyfikasi menggunakan logika fuzzy "or" (max) MAMDANI
	def defuzzyfikasi(self, fuzzy_outputs):
		return np.mean(fuzzy_outputs)

	def calculate(self, info, w, pid, pError):

		error = info[0][0] - w // 2
		if info[0][0] != 0:
			# Contoh penggunaan
			# target_value = 10.0
			# prev_error = 0.0

			# Simulasikan proses membaca sensor
			# current_value = 10.0 + (2.0 * (0.5 - time.time() % 1.0))
			
			# error = target_value - current_value
			d_error = error - pError
			# pError = error
			print("fuzzy 1 ", error)
			print("fuzzy 2 ", pError)
			print("fuzzy 3 ", d_error)
			# Proses fuzzyfikasi
			fuzzy_outputs = self.fuzzyfikasi(error, d_error, self.membership_functions)
			print("fuzzy a ", fuzzy_outputs)
			# Proses defuzzyfikasi
			output = self.defuzzyfikasi(fuzzy_outputs)

			print("fuzzy b", output)
		return error
