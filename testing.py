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
		self.speed = [500,1200]
		self.error = [40,80]
		self.delta = [40,50,60]

	def f_low(self,x):
		if x>= self.error[1]:
			return 0
		if x >= self.error[0] and x <= self.error[1]:
			return (self.error[1]-x)/(self.error[1]-self.error[0])
		if x<=self.error[0] :
			return 1

	def f_high(self,x):
		if x>= self.error[1]:
			return 1
		if x >= self.error[0] and x <= self.error[1]:
			return (x-self.error[0])/(self.error[1]-self.error[0])
		if x<= self.error[0] :
			return 0

	def f_d_low(self,x):
		if x>= self.delta[1]:
			return 0
		if x >= self.delta[0] and x <=self.delta[1]:
			return (self.delta[1] - x)/(self.delta[1]-self.delta[0])
		if x <= self.delta[0]:
			return 1

	def f_d_med(self,x):
		if x <= self.delta[0] or x >= self.delta[2]:
			return 0
		if x >= self.delta[0] and x <= self.delta[1]:
			return (x-self.delta[0])/(self.delta[1]-self.delta[0])
		if x >= self.delta[1] and x <= self.delta[2]:
			return (self.delta[2]-x)/(self.delta[2]-self.delta[1])

	def f_d_high(self,x):
		if x <= self.delta[1]:
			return 0
		if x >= self.delta[1] and x <= self.delta[2]:
			return (x-self.delta[1])/(self.delta[2]-self.delta[1])
		if x >= self.delta[2]:
			return 1

	# def slow(x):
	# 	if x >= speed[1]:
	# 		return 0
	# 	if x<= speed[0] and x<speed[1]:
	# 		return (speed[1]-x)/(speed[1]-speed[0])
	# 	if x < speed[0]:
	# 		return 1

	# def fast(x):
	# 	if x >= speed[1]:
	# 		return 1
	# 	if x <= speed[0] and x < speed[1]:
	# 		return (x-speed[0])/(speed[1]-speed[0])
	# 	if x < speed[0]:
	# 		return 0

	def f(self, val,z=1):
		return val * z

	def f_miring(self, val, z1, z2=1):
		return (z1-val[0])/(val[1]-val[0])*z2

	def simson_integral(self, f, a, b, val, isZ = True, n=100):
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

	def simson_integral_miring(self, f, a, b, val, isZ = True, n=100):
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


	def update(self , err, delta):
		
		r_e_low = self.f_low(err)
		r_e_high = self.f_high(err)

		r_d_low = self.f_d_low(delta)
		r_d_med = self.f_d_med(delta)
		r_d_high = self.f_d_high(delta)

		print(r_e_low ,r_e_high)
		print(r_d_low, r_d_med, r_d_high)

		rule_base = [
					(min(r_e_low, r_d_low), 'slow'),
					(min(r_e_low, r_d_med), 'slow'),
					(min(r_e_low, r_d_high), 'fast'),

					(min(r_e_high, r_d_low), 'slow'),
					(min(r_e_high, r_d_med), 'fast'),
					(min(r_e_high, r_d_high), 'fast'),
				]
				
		slow = []
		fast = []
		print()
		for rule in rule_base:
			print(rule)
			if rule[1] == "slow":
				slow.append(rule[0])
			if rule[1] == "fast":
				fast.append(rule[0])

		inference = [max(slow), max(fast)]
		print()
		print(inference)
		print()

		t1 = (inference[0]*(self.speed[1]- self.speed[0])) + self.speed[0]
		t2 = (inference[1]*(self.speed[1]- self.speed[0])) + self.speed[0]
		# print(t1,t2)

		# M1 = self.simson_integral(self.f,0, t1, inference[0])
		# M2 = self.simson_integral_miring(self.f, t1, t2, [self.speed[0],self.speed[1] ])
		# M3 = self.simson_integral(self.f, t2, self.speed[1], inference[1])
		# print(M1, M2 , M3)
		# A1 = self.simson_integral(self.f,0, t1, inference[0], False)
		# A2 = self.simson_integral_miring(self.f, t1, t2, [self.speed[0],self.speed[1] ], False)
		# A3 = self.simson_integral(self.f, t2, self.speed[1], inference[1], False)
		# print(A1, A2 , A3)


		t_M1 = ThreadWithReturnValue(target=self.simson_integral, 			args=( self.f, 0, t1, inference[0])) 
		t_M2 = ThreadWithReturnValue(target=self.simson_integral_miring,	args=( self.f, t1, t2, [self.speed[0], self.speed[1]])) 
		t_M3 = ThreadWithReturnValue(target=self.simson_integral, 			args=( self.f, t2, self.speed[1], inference[1]))  
	
		t_A1 = ThreadWithReturnValue(target=self.simson_integral, 			args=(self.f, 0, t1, inference[0], False))
		t_A2 = ThreadWithReturnValue(target=self.simson_integral_miring,	args=(self.f, t1, t2, [self.speed[0],self.speed[1]], False))
		t_A3 = ThreadWithReturnValue(target=self.simson_integral, 			args=(self.f, t2, self.speed[1], inference[1], False))
		t_M1.start() 
		t_M2.start() 
		t_M3.start() 

		M1 = t_M1.join() 
		M2 = t_M2.join() 
		M3 = t_M3.join() 

		t_A1.start() 
		t_A2.start() 
		t_A3.start() 


		A1 = t_A1.join() 
		A2 = t_A2.join() 
		A3 = t_A3.join() 
		numerator = (M1 + M2 + M3)
		denominator =  (A1 + A2 +A3)

		output = 0

		if denominator != 0:
			output = int(numerator/ denominator)
		print(output)

fuzz = Fuzzy()
fuzz.update(50, 58)