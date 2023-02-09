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
		\      /
		 \    /
		  \  /
		   \/
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

	def update(self, current_error):

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
			output = defuzzified_value / total_weight
		return int(-output)
