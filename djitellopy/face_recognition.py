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
	
	# integral = 0

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

	def find_face(self, frame, comb_face, selectedX, selectedY):
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = self.faceCascade.detectMultiScale(
			gray,
			scaleFactor=1.35,
			minNeighbors=5,
			minSize=(60, 60))
		index = comb_face.current()

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

			id_1 = id == self.names[1] # and index == 0
			id_2 = id == self.names[2] # and index == 1
			id_3 = id == self.names[3] # and index == 2
			id_4 = id == self.names[4] # and index == 3
			id_5 = id == self.names[5] # and index == 4

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
				return frame,  [[0, 0], 0]

		if len(myFaceListArea) != 0:
			i = myFaceListArea.index(max(myFaceListArea))
			return frame, [myFaceListC[i], myFaceListArea[i]]
		else:
			return frame, [[0, 0], 0]
