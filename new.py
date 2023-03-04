'''
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

inferensi
                __________
		   	   /
		   ___/
		 /    
________/     
    M1  M2 M3 M4  M5

    -50    0    50
'''

v_min = 0
v_med = 50
v_max = 100

e_low = [0, 25, 50]
e_med = [25, 50, 100]
e_high = [50, 100, 200]

def triangular_mf(x, a, b, c):
	if x <= a:
		return 0
	elif x > a and x < b:
		return (x - a) / (b - a)
	elif x >= b and x < c:
		return (c - x) / (c - b)
	else:
		return 0

def f(val,z=1):
    return val * z

def f_miring(val, z1, z2=1):
    return (z1-val[0])/(val[1]-val[0])*z2

def simson_integral(f, a, b, val, isZ = True, n=100):
	h = (b-a) / n
	x = [a+i*h for i in range(n+1)]
	if isZ:
		fx = [f(val, x[i]) for i in range(n+1)]
	else:
		fx = [f(val) for i in range(n+1)]
    
	integral = fx[0] + fx[n] # jumlahkan f(a) dan f(b)
	for i in range(1, n, 2): # loop untuk f ganjil
		integral += 4 * fx[i]
	for i in range(2, n-1, 2): # loop untuk f genap
		integral += 2 * fx[i]
	integral *= h / 3 # faktor Simson

	return integral

def simson_integral_miring(f, a, b, val, isZ = True, n=100):
	h = (b-a) / n
	x = [a+i*h for i in range(n+1)]
	if isZ :
		fx = [f_miring(val, x[i], x[i]) for i in range(n+1)]
	else:
		fx = [f_miring(val, x[i]) for i in range(n+1)]

	integral = fx[0] + fx[n] # jumlahkan f(a) dan f(b)
	for i in range(1, n, 2): # loop untuk f ganjil
		integral += 4 * fx[i]
	for i in range(2, n-1, 2): # loop untuk f genap
		integral += 2 * fx[i]
	integral *= h / 3 # faktor Simson
    
	return integral

def	proses(err, delta):

	r_e_low = triangular_mf(err, e_low[0],  e_med[0], e_high[0])
	r_e_med = triangular_mf(err, e_low[1],  e_med[1], e_high[1])
	r_e_high = triangular_mf(err, e_low[2],  e_med[2], e_high[2])

	r_d_low = triangular_mf(delta, e_low[0],  e_med[0], e_high[0])
	r_d_med = triangular_mf(delta, e_low[1],  e_med[1], e_high[1])
	r_d_high = triangular_mf(delta, e_low[2],  e_med[2], e_high[2])
	
	print(r_e_low)
	print(r_e_med)
	print(r_e_high)
	print()
	print(r_d_low)
	print(r_d_med)
	print(r_d_high)
	print()
	# Rule base
	rule_base = [
		(min(r_e_low, r_d_low), 'fast'),
		(min(r_e_low, r_d_med), 'normal'),
		(min(r_e_low, r_d_high), 'slow'),

		(min(r_e_med, r_d_low), 'fast'),
		(min(r_e_med, r_d_med), 'normal'),
		(min(r_e_med, r_d_high), 'slow'),

		(min(r_e_high, r_d_low), 'fast'),
		(min(r_e_high, r_d_med), 'normal'),
		(min(r_e_high, r_d_high), 'slow')
	]
	
	slow = []
	medium = []
	fast = []

	for rule in rule_base:
		print(rule)
		if rule[1] == "slow":
			slow.append(rule[0])
		if rule[1] == "normal":
			medium.append(rule[0])
		if rule[1] == "fast":
			fast.append(rule[0])
			
	print()

	inference = [max(slow),max(medium), max(fast)]
	print(inference)
	point1 = (inference[0]*(v_med-v_min)) + v_min
	point2 = (inference[1]*(v_med-v_min)) + v_min
	point3 = (inference[1]*(v_max-v_med)) + v_med
	point4 = (inference[2]*(v_max-v_med)) + v_med

	print("p1 ",point1)
	print("p2 ",point2)
	print("p3 ",point3)
	print("p4 ",point4)
	print()

	M1 = simson_integral(f,0, point1, inference[0])
	M2 = simson_integral_miring(f, point1, point2, [v_min,v_med])
	M3 = simson_integral(f, point2, point3, inference[1])
	M4 = simson_integral_miring(f, point3, point4, [v_med,v_max])
	M5 = simson_integral(f, point3, point4, inference[2])
	print("M1 ", M1)
	print("M2 ", M2)
	print("M3 ", M3)
	print("M4 ", M4)
	print("M5 ", M5)

	print()

	A1 = simson_integral(f,0, point1, inference[0], False)
	A2 = simson_integral_miring(f, point1, point2, [v_min,v_med], False)
	A3 = simson_integral(f, point2, point3, inference[1], False)
	A4 = simson_integral_miring(f, point3, point4, [v_med,v_max], False)
	A5 = simson_integral(f, point3, point4, inference[2], False)
	print("A1 ", A1)
	print("A2 ", A2)
	print("A3 ", A3)
	print("A4 ", A4)
	print("A5 ", A5)

	centroid = (M1+M2+M3+M4+M5) / (A1+A2+A3+A4+A5)
	print(centroid)

proses(10, 1)


