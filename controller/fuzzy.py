'''
	Fuzzy logic Mamdani
	Danu andrean
	2023

----------------------------
condition
	   /\   /\   /\	
	  /  \ /  \ /  \	
	 /    \    \    \	
	/    / \  / \    \		

       -     0     +
speed
________        __________
		\  /\  /
		 \/  \/
		 /\  /\
________/__\/__\__________
    -50    0    50

inference
                __________
		   	   /
		   ___/
		 /    
________/     
    M1  M2 M3 M4  M5
	
    -50    0    50
'''

from threading import Thread

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return

class Fuzzy:
	def __init__(self):
		self.previous_error = 0
		self.negative = 0
		self.normal = 0
		self.positive = 0
		self.speed = 0

	def set(self, negative, normal, positive,
					 d_low, d_normal, d_high, speed):

		self.negative = negative
		self.normal = normal
		self.positive = positive
		self.d_low = d_low
		self.d_normal = d_normal
		self.d_high = d_high

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
	
	def f(self, val,z=1):
		return val * z

	def f_miring(self, val, z1, z2=1):
		return (z1-val[0])/(val[1]-val[0])*z2

	def simson_integral(self, f, a, b, val, isZ = True, n=1):
		h = (b-a) / n
		x = [a+i*h for i in range(n+1)]
		if isZ:
			fx = [self.f(val, x[i]) for i in range(n+1)]
		else:
			fx = [self.f(val) for i in range(n+1)]
		
		integral = fx[0] + fx[n] 	# jumlahkan f(a) dan f(b)
		for i in range(1, n, 2): 	# loop untuk f ganjil
			integral += 4 * fx[i]
		for i in range(2, n-1, 2): 	# loop untuk f genap
			integral += 2 * fx[i]
		integral *= h / 3 			# faktor Simson

		# out_queue.put(integral)
		return integral

	def simson_integral_miring(self, f, a, b, val, isZ = True, n=1):
		h = (b-a) / n
		x = [a+i*h for i in range(n+1)]
		if isZ :
			fx = [self.f_miring(val, x[i], x[i]) for i in range(n+1)]
		else:
			fx = [self.f_miring(val, x[i]) for i in range(n+1)]

		integral = fx[0] + fx[n] 	# jumlahkan f(a) dan f(b)
		for i in range(1, n, 2): 	# loop untuk f ganjil
			integral += 4 * fx[i]
		for i in range(2, n-1, 2): 	# loop untuk f genap
			integral += 2 * fx[i]
		integral *= h / 3 			# faktor Simson
		
		# out_queue.put(integral)
		return integral

	def update(self, current_error, mode):
		if(current_error == 0):
			current_error = 1

		delta_error = current_error - self.previous_error  

		self.previous_error = current_error

		# Fuzzyfication
		# Membership function for error
		r_e_low 	= self.triangular_mf(current_error, self.negative[0], self.normal[0], self.positive[0])
		r_e_med 	= self.triangular_mf(current_error, self.negative[1], self.normal[1], self.positive[1])
		r_e_high 	= self.triangular_mf(current_error, self.negative[2], self.normal[2], self.positive[2])

		# Membership function for delta_error
		r_d_low 	= self.triangular_mf(delta_error, self.d_low[0], self.d_normal[0], self.d_high[0])
		r_d_med		= self.triangular_mf(delta_error, self.d_low[1], self.d_normal[1], self.d_high[1])
		r_d_high	= self.triangular_mf(delta_error, self.d_low[2], self.d_normal[2], self.d_high[2])

		# Rule base

		rule_base = [
			(min(r_e_low, r_d_low), 'slow'),
			(min(r_e_low, r_d_med), 'slow'),
			(min(r_e_low, r_d_high), 'slow'),

			(min(r_e_med, r_d_low), 'normal'),
			(min(r_e_med, r_d_med), 'normal'),
			(min(r_e_med, r_d_high), 'normal'),

			(min(r_e_high, r_d_low), 'fast'),
			(min(r_e_high, r_d_med), 'fast'),
			(min(r_e_high, r_d_high), 'fast')
		]
		
		slow = []
		medium = []
		fast = []

		for rule in rule_base:
			# print(rule)
			if rule[1] == "slow":
				slow.append(rule[0])
			if rule[1] == "normal":
				medium.append(rule[0])
			if rule[1] == "fast":
				fast.append(rule[0])

		inference = [max(slow),max(medium), max(fast)]

		point1 = (inference[0]*(0-self.speed[0])) + self.speed[0]
		point2 = (inference[1]*(0-self.speed[0])) + self.speed[0]
		point3 = (inference[1]*(self.speed[1]-0)) + 0
		point4 = (inference[2]*(self.speed[1]-0)) + 0


		t_M1 = ThreadWithReturnValue(target=self.simson_integral, 			args=( self.f, 0, point1, inference[0])) 
		t_M2 = ThreadWithReturnValue(target=self.simson_integral_miring,	args=( self.f, point1, point2, [self.speed[0],0])) 
		t_M3 = ThreadWithReturnValue(target=self.simson_integral, 			args=( self.f, point2, point3, inference[1])) 
		t_M4 = ThreadWithReturnValue(target=self.simson_integral_miring,	args=( self.f, point3, point4, [0,self.speed[1]])) 
		t_M5 = ThreadWithReturnValue(target=self.simson_integral, 			args=( self.f, 0, point3, point4, inference[2])) 
	
		t_A1 = ThreadWithReturnValue(target=self.simson_integral, 			args=(self.f, 0, point1, inference[0], False))
		t_A2 = ThreadWithReturnValue(target=self.simson_integral_miring,	args=(self.f, point1, point2, [self.speed[0],0], False))
		t_A3 = ThreadWithReturnValue(target=self.simson_integral, 			args=(self.f, point2, point3, inference[1], False))
		t_A4 = ThreadWithReturnValue(target=self.simson_integral_miring,	args=(self.f, point3, point4, [0,self.speed[1]], False))
		t_A5 = ThreadWithReturnValue(target=self.simson_integral, 			args=(self.f, point3, point4, inference[2], False))
		
		t_A1.start() 
		t_A2.start() 
		t_A3.start() 
		t_A4.start() 
		t_A5.start()

		t_M1.start() 
		t_M2.start() 
		t_M3.start() 
		t_M4.start() 
		t_M5.start()

		M1 = t_M1.join() 
		M2 = t_M2.join() 
		M3 = t_M3.join() 
		M4 = t_M4.join() 
		M5 = t_M5.join() 

		A1 = t_A1.join() 
		A2 = t_A2.join() 
		A3 = t_A3.join() 
		A4 = t_A4.join() 
		A5 = t_A5.join() 

		numerator = M1+M2+M3+M4+M5
		denominator = A1+A2+A3+A4+A5
		output = 0.0

		if denominator != 0.0:
			output = numerator/ denominator

		# 	print(output, "centroid")
		
		# data return
		ret_error	= 0
		ret_delta 	= 0
		ret_speed	= 0


		if mode:
			ret_error	= current_error
			ret_delta 	= delta_error
			ret_speed	= output
		else:
			max_err = r_e_low
			ret_error = self.negative[0]
			if r_e_med > max_err:
				max_err = r_e_med
				ret_error = self.normal[1]
			if r_e_high > max_err:
				max_err = r_e_high
				ret_error = self.positive[2]

			max_delta = r_e_low
			ret_delta = self.negative[0]
			if r_e_med > max_delta:
				max_delta = r_e_med
				ret_delta = self.normal[1]
			if r_e_high > max_delta:
				max_delta = r_e_high
				ret_delta = self.positive[2]

			low = (self.speed[1]- self.speed[0])/3
			if output<= (low+self.speed[0]):
				ret_speed = self.speed[0]
			if output > (low+self.speed[0]):
				ret_speed = 0
			if output >self.speed[0]+(low+low):
				ret_speed = self.speed[1]
		return output, ret_error, ret_delta, ret_speed
