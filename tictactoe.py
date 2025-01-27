# IC 6101 1er Semestre 2017
# Nombre: Wilberth Castro
# Correo: wilz04@gmail.com

# Un estado "abcdefghi" corresponde al tablero:
# a b c
# d e f
# g h i
# 
# Encabezado del archivo rewd.csv:
# Estado; Valor
# 
# Encabezado del archivo prob.csv:
# Estado Origen; Estado Destino; Probabilidad
# 
# Encabezado del archivo pi.csv:
# Estado; Accion

prob = {}
rewd = {}
pi = {}


def fact(n, m):
	if n > m:
		return n*fact(n-1, m)
	else:
		return n

def dist(n):
	if n == 9:
		return 1.0/n
	else:
		return 1.0/(9.0**(10-n)*fact(8, n))

def state_eval(state):
	goals = (
		(0, 1, 2),
		(3, 4, 5),
		(6, 7, 8),
		(0, 3, 6),
		(1, 4, 7),
		(2, 5, 8),
		(0, 4, 8),
		(2, 4, 6)
	)
	
	for goal in goals:
		if state[goal[0]] == state[goal[1]] and state[goal[1]] == state[goal[2]]:
			if state[goal[0]] == '1':
				return 1
			elif state[goal[0]] == '2':
				return -1
	
	return 0

def load_probs_rewards_pi(state, depth):
	rewd[state] = state_eval(state)
	if depth == 0 or rewd[state] != 0:
		return rewd[state]
	
	agent = 2-depth%2
	value = (-1)**agent
	
	for i in range(0, 9):
		if state[i] != '0': continue
		
		if state not in pi.keys():
			pi[state] = i
		
		tmp = list(state)
		tmp[i] = agent
		new_state = "".join(str(j) for j in tmp)
		
		if state not in prob.keys():
			prob[state] = {}
		
		prob[state][new_state] = dist(depth)
		
		rewd[new_state] = state_eval(new_state)
		if rewd[new_state] != 0:
			if agent == 1:
				if rewd[new_state] > value:
					value = rewd[new_state]
					pi[state] = i
				# value = max(rewd[new_state], value)
			else:
				if rewd[new_state] < value:
					value = rewd[new_state]
					pi[state] = i
				# value = min(rewd[new_state], value)
			continue
		
		rewd[new_state] = load_probs_rewards_pi(new_state, depth-1)
		if agent == 1:
			if rewd[new_state] > value:
				value = rewd[new_state]
				pi[state] = i
			# value = max(rewd[new_state], value)
		else:
			if rewd[new_state] < value:
				value = rewd[new_state]
				pi[state] = i
			# value = min(rewd[new_state], value)
		
	rewd[state] = value
	return value

def print_rewd():
	buffer = ""
	for state in rewd.keys():
		buffer += state + "; " + str(rewd[state]) + "\n"
	
	file = open("rewd.csv", "w")
	file.write(buffer + "\n")
	file.close()
	# print buffer;

def print_prob():
	buffer = ""
	for state_1 in prob.keys():
		for state_2 in prob[state_1].keys():
			buffer += state_1 + "; " + state_2 + "; " + str(prob[state_1][state_2]) + "\n"
	
	file = open("prob.csv", "w")
	file.write(buffer + "\n")
	file.close()
	# print buffer;

def print_pi():
	buffer = ""
	for state in pi.keys():
		buffer += state + "; " + str(pi[state]) + "\n"
	
	file = open("pi.csv", "w")
	file.write(buffer + "\n")
	file.close()
	# print buffer;

def main():
	load_probs_rewards_pi("000000000", 9)
	
	# print state_eval("111000000")
	print_rewd()
	print_prob()
	print_pi()

main()
