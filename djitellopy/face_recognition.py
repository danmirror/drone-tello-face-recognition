
import cv2

class Face_Recognition:
	cap= cv2.VideoCapture(0)
	names = ['None', 'Dian', 'Yossi',"Fahmizal","Alim", "Matthew"]

	def __init__(self):


		# self.myDrone.connect()
		# self.myDrone.for_back_velocity = 0
		# self.myDrone.left_right_velocity = 0
		# self.myDrone.up_down_velocity = 0
		# self.myDrone.yaw_velocity = 0
		# self.myDrone.speed = 0
		# print("Battery > ",self.myDrone.get_battery())
		# self.myDrone.streamoff()
		# self.myDrone.streamon()

		print("hello")


	def get_frame(self, w, h):
		# frame = self.myDrone.get_frame_read().frame
		ret, frame = self.cap.read()
		# frame = cv2.flip(frame, 1)
		frame = cv2.resize(frame, (w, h))
		return frame

	def find_face(self, frame, faceCascade, comb_index, recognizer):
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

			if id == self.names[1] :#and index == 0:  # Alim
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				cv2.putText(frame, str(id), (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
				cv2.putText(frame, str(confidence), (x + 5, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1)
				# selectedX.set(x1_text)
				# selectedY.set(y1_text)
				# string = 'X{0:d}Y{1:d}'.format(x_pos, y_pos)
				# arduino.write(string.encode('utf-8',errors="ignore"))

			elif id == self.names[2] :#and index == 1:  # Matthew
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				cv2.putText(frame, str(id), (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
				cv2.putText(frame, str(confidence), (x + 5, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1)
				# selectedX.set(x1_text)
				# selectedY.set(y1_text)
				# string = 'X{0:d}Y{1:d}'.format(x_pos, y_pos)
				# arduino.write(string.encode('utf-8',errors="ignore"))

			elif id == self.names[3] :#and index == 2:  # Dian
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				cv2.putText(frame, str(id), (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
				cv2.putText(frame, str(confidence), (x + 5, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1)
				# selectedX.set(x1_text)
				# selectedY.set(y1_text)
				# string = 'X{0:d}Y{1:d}'.format(x_pos, y_pos)
				# arduino.write(string.encode('utf-8',errors="ignore"))

			elif id == self.names[4] :#and index == 3:  # Yossi
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				cv2.putText(frame, str(id), (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
				cv2.putText(frame, str(confidence), (x + 5, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1)
				# selectedX.set(x1_text)
				# selectedY.set(y1_text)
				# string = 'X{0:d}Y{1:d}'.format(x_pos, y_pos)
				# arduino.write(string.encode('utf-8',errors="ignore"))

			elif id == self.names[5] :#and index == 4:  # Fahmizal
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				cv2.putText(frame, str(id), (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
				cv2.putText(frame, str(confidence), (x + 5, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1)
				# selectedX.set(x1_text)
				# selectedY.set(y1_text)
				# string = 'X{0:d}Y{1:d}'.format(x_pos, y_pos)
				# arduino.write(string.encode('utf-8',errors="ignore"))
			else:
				return frame, False
		return frame, True
