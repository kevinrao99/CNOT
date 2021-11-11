import collections
import cnot_util

def target_copy():
	global target
	ans = []

	for i in range(N):
		new_row = []
		for j in range(N):
			if target[i][j] == 1:
				new_row.append(1)
			else:
				new_row.append(0)
		ans.append(new_row)
	return ans

def extend(op_list):
	global N
	global left_queue
	global right_queue
	for i in range(1, N + 1):
		for j in range(1, N + 1):
			if i == j:
				continue

			if len(op_list) > 0:
				(a, b) = op_list[len(op_list) - 1]

				# if i, j, a, b are all distinct, order by i and a
				# if i =/= a and j == b, order by i and a
				# if i == a and j =/= b, order by j and b
				# if i == a and j == b, do nothing

				
				if not (i == a) and not (i == b) and not (j == a):
					if i > a:
						continue
				elif i == a:
					if j >= b:
						continue
				'''

				if i == a and j == b:
					continue # Temporarily removing some optimization for testing
				'''
				

			left_queue.append(op_list + [(i, j)])
			right_queue.append(op_list + [(i, j)])

def direction_modular(dir_queue, store_queue, direction):
	global reached
	global middle_matrices
	global N

	met_in_middle = False

	while len(dir_queue) > 0:
		cur = dir_queue.popleft()

		if direction == 0:
			store_queue.append(cur)

		matrix_ops = None
		matrix_hash = 0

		if direction == 0:
			matrix_ops = cnot_util.perform_ops(cnot_util.identity(N), cur)
		else:
			matrix_ops = cnot_util.perform_ops(target_copy(), cur)

		matrix_hash = cnot_util.matrix_to_int(matrix_ops)

		if matrix_hash in reached:
			reached_list = reached[matrix_hash]

			# Check if met in the middle
			for (reach_dir, reach_ops) in reached_list:
				if not (reach_dir == direction):
					met_in_middle = True
					middle_matrices[matrix_hash] = 1

			reached[matrix_hash].append((direction, cur))

		else:
			reached[matrix_hash] = [(direction, cur)]
			# print reached[matrix_hash]

	return met_in_middle

def bfs():
	global left_queue
	global right_queue
	global reached
	global middle_matrices

	left_queue = collections.deque([])
	right_queue = collections.deque([])
	reached = dict({}) # dict mapping matrix hashes to a list of (a, b) where a is direction and b is the operations from the direction to the matrix
	middle_matrices = dict({}) # dict mapping matrix hashes to 1 if the matrix was reached from both sides

	left_queue.append([])
	right_queue.append([])

	store_queue = collections.deque([])

	while True:

		if direction_modular(left_queue, store_queue, 0):
			break

		if direction_modular(right_queue, store_queue, 1):
			break

		print len(store_queue)

		while len(store_queue) > 0:
			to_extend = store_queue.popleft()
			extend(to_extend)

	# Now reached should have a key for every matrix seen in the meet in middle algorithm and middle matrices should have all the ones in the middle
	# Only need to reconstruct all the paths from here

	ans_list = []

	middle_hashes = middle_matrices.keys()
	for matrix_hash in middle_hashes:
		reached_list = reached[matrix_hash]

		for (a, a_ops) in reached_list:
			for (b, b_ops) in reached_list:
				if not (a == 0 and b == 1):
					continue

				to_append = []
				for (r1, r2) in a_ops:
					to_append.append((r1, r2))

				for i in range(len(b_ops)):
					to_append.append(b_ops[len(b_ops) - i - 1])

				ans_list.append(to_append)

	return ans_list

def trim_trivial(ans_list):
	trimmed_ans_list = []

	for op_list in ans_list:

		print op_list

		append = True
		for index in range(len(op_list) - 1):
			(a, b) = op_list[index]
			(i, j) = op_list[index + 1]

			if not (i == a) and not (i == b) and not (j == a):
				if i > a:
					append = False
					print "i >  a, i = " + str(i) + ", a = ", str(a)
			elif i == a:
				if j >= b:
					append = False
					print "j >= b, j = " + str(j) + ", b = ", str(b)

		if append:
			trimmed_ans_list.append(op_list)

	return trimmed_ans_list	

def this_run_target():

	'''
	target = [[1, 1, 1, 1, 1, 1, 1, 1],
			  [0, 1, 0, 1, 0, 1, 0, 1],
			  [0, 0, 1, 1, 0, 0, 1, 1],
			  [0, 0, 0, 1, 0, 0, 0, 1],
			  [0, 0, 0, 0, 1, 1, 1, 1],
			  [0, 0, 0, 0, 0, 1, 0, 1],
			  [0, 0, 0, 0, 0, 0, 1, 1],
			  [0, 0, 0, 0, 0, 0, 0, 1],
	]
	
	
	target = [[1, 0, 1, 0, 0, 1, 1],
			  [0, 1, 1, 0, 0, 0, 1],
			  [0, 0, 1, 0, 0, 1, 0],
			  [0, 0, 0, 1, 1, 1, 1],
			  [0, 0, 0, 0, 1, 0, 1],
			  [0, 0, 0, 0, 0, 1, 0],
			  [0, 0, 0, 0, 0, 0, 1]
	]
	
	
	target = [[1, 0, 0, 0, 1, 1],
			  [0, 1, 0, 1, 0, 1],
			  [0, 0, 1, 1, 1, 1],
			  [0, 0, 0, 1, 1, 0],
			  [0, 0, 0, 0, 1, 0],
			  [0, 0, 0, 0, 0, 1]
	]

	
	target = [[0, 1, 1, 1, 1, 1],
			  [1, 0, 1, 1, 1, 1],
			  [1, 1, 0, 1, 1, 1],
			  [1, 1, 1, 0, 1, 1],
			  [1, 1, 1, 1, 0, 1],
			  [1, 1, 1, 1, 1, 0]
	]
	
	
	target = [[0, 1, 1, 1, 1],
			  [1, 0, 1, 1, 1],
			  [1, 1, 0, 1, 1],
			  [1, 1, 1, 0, 1],
			  [1, 1, 1, 1, 0]
	]

	'''
	target = [[1, 1, 1, 1, 1],
			  [1, 0, 1, 1, 1],
			  [1, 1, 0, 1, 1],
			  [1, 1, 1, 0, 1],
			  [1, 1, 1, 1, 0]
	]
	'''
	target = [[1, 1, 0, 1],
			  [0, 1, 1, 1],
			  [0, 0, 1, 0],
			  [0, 0, 0, 1]

	]
	
	target = [[0, 1, 1, 1],
			  [1, 0, 1, 1],
			  [1, 1, 0, 1],
			  [1, 1, 1, 0]
	]


	'''
	return target

def check_all_neighbors():
	global target
	global N

	ans_list = bfs()
	target_complexity = len(ans_list[0])

	for i in range(1, N + 1):
		for j in range(1, N + 1):
			if i == j:
				continue

			cnot_util.operation(target, i, j)

			neighbor_ans_list = bfs()
			neighbor_complexity = len(neighbor_ans_list[0])
			if neighbor_complexity > target_complexity:
				return False

			cnot_util.operation(target, i, j)

	return True




if __name__ == '__main__':
	# Identity on the l, target on the r, meet in the middle
	global target
	global N


	target = this_run_target()
	N = len(target)
	print "Searching for target:"

	for i in range(N):
		for j in range(N):
			print str(target[i][j]) + " ",
		print

	print "Target is local max is " + str(check_all_neighbors())
	








