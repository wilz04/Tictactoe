theta = 1*10**-7
V = {}

def wins(n):
	stat = (0, 222.0, 1392.0, 4116.0)
	prob = .0
	for i in range(n, 4):
		prob += 8.0/stat[i]
	
	return prob

def policy_eval(state, depth, diff):
	if depth == 0 or state_eval(state) != 0:
		return diff
	
	for i in range(0, 9):
		if state[i] != '0': continue
		
		tmp = list(state)
		tmp[i] = agent
		new_state = "".join(str(j) for j in tmp)
		
		if state not in V.keys():
			V[state] = {}
		
		if state_eval(new_state) != 0:
			old_val = V[state][new_state]
			V[state][new_state] = backup_action(state, new_state, policy[state][new_state])
			diff = max(diff, abs(V[state][new_state] - old_val))
			continue
		
		policy_eval(new_state, depth-1, diff)
		
	return diff

def policy_eval():
	val_tmp = .0
	diff = 1.0
	a = 0
	while diff > theta:
		diff = .0
		for n1 in range(10, 1, -1):
			for n2 in range(9, 0, -1):
				val_tmp = V[n1][n2]
				a = policy[n1][n2]
				V[n1][n2] = backup_action(n1, n2, a)
				diff = max(diff, abs(V[n1][n2] - val_tmp))

def backup_action(n1, n2, a):
	val = 0
	morning_n1 = n1 - a
	morning_n2 = n2 + a
	for state_1 in prob.keys():
		for state_2 in prob[state_1].keys():
			val += prob[state_1][state_2]*(rewd[state_2] + discount*V[state_2])
			
		for new_n2 in range(0, ncar_states):
			val += prob_1[morning_n1][new_n1]*prob_2[morning_n2][new_n2] * (rew_1[morning_n1] + rew_2[morning_n2] + discount*V[new_n1][new_n2])
	
	return val