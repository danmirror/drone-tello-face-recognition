'''
	Fuzzy logic 
	Danu andrean
	2023


----------------------------
condition
	   /\   /\   /\	
	  /  \ /  \ /  \	
	 /    \    \    \	
	/    / \  / \    \		

       -     0     +
-----------------------------
speed
________        __________
		\  /\  /
		 \/  \/
		 /\  /\
________/__\/__\__________
    -50    0    50

'''


class Fuzzy:
	def __init__(self):
		self.previous_error = 0
		self.negative = 0
		self.normal = 0
		self.positive = 0
		self.speed = 0

	def set(self, negative, normal, positive, speed):
		self.negative = negative
		self.normal = normal
		self.positive = positive
		self.speed = speed
	
	def clear(self):
		self.previous_error = 0

	def triangular_mf(self, x, a, b, c):
		if x <= a:
			return 0
		elif x > a and x < b:
			return (x - a) / (b - a)
		elif x >= b and x < c:
			return (c - x) / (c - b)
		else:
			return 0

	def update(self, current_error, mode):

		average_error = (current_error + self.previous_error) //2  
		self.previous_error = current_error

		# Fuzzyfication
		# Membership function for error
		error_low 		= self.triangular_mf(current_error, self.negative[0], self.normal[0], self.positive[0])
		error_medium 	= self.triangular_mf(current_error, self.negative[1], self.normal[1], self.positive[1])
		error_high 		= self.triangular_mf(current_error, self.negative[2], self.normal[2], self.positive[2])

		# Membership function for average_error
		average_negatif = self.triangular_mf(average_error, self.negative[0], self.normal[0], self.positive[0])
		average_nol		= self.triangular_mf(average_error, self.negative[1], self.normal[1], self.positive[1])
		average_positif	= self.triangular_mf(average_error, self.negative[2], self.normal[2], self.positive[2])

		# Rule base
		rule_base = [
			(min(error_low, average_negatif), 'fast'),
			(min(error_low, average_nol), 'normal'),
			(min(error_low, average_positif), 'slow'),
			(min(error_medium, average_negatif), 'fast'),
			(min(error_medium, average_nol), 'normal'),
			(min(error_medium, average_positif), 'normal'),
			(min(error_high, average_negatif), 'normal'),
			(min(error_high, average_nol), 'slow'),
			(min(error_high, average_positif), 'slow')
		]

		# Defuzzification
		defuzzified_value = 0
		total_weight = 0
		for r in rule_base:
			weight = r[0]
			if weight > 0:
				if r[1] == 'slow':
					defuzzified_value += weight * self.speed[0]
					total_weight += weight
				elif r[1] == 'normal':
					defuzzified_value += weight * 0
					total_weight += weight
				elif r[1] == 'fast':
					defuzzified_value += weight * self.speed[1]
					total_weight += weight
				
		output = 0
		if not total_weight ==  0:
			output = int(-(defuzzified_value / total_weight))
		
		
		# data return
		ret_error	= 0
		ret_average = 0
		ret_speed	= 0


		if mode:
			ret_error	= current_error
			ret_average = average_error
			ret_speed	= -output
			print("mode true")
		else:
			max_err = error_low
			ret_error = self.negative[0]
			if error_medium > max_err:
				max_err = error_medium
				ret_error = self.normal[1]
			if error_high > max_err:
				max_err = error_high
				ret_error = self.positive[2]

			max_average = error_low
			ret_average = self.negative[0]
			if error_medium > max_average:
				max_average = error_medium
				ret_average = self.normal[1]
			if error_high > max_average:
				max_average = error_high
				ret_average = self.positive[2]

			low = (self.speed[1]- self.speed[0])/3
			if output<= (low+self.speed[0]):
				ret_speed = self.speed[0]
			if output > (low+self.speed[0]):
				ret_speed = 0
			if output >self.speed[0]+(low+low):
				ret_speed = self.speed[1]
		return output, ret_error, ret_average, ret_speed
