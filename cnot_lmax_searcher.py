import collections
import cnot_util

def find_lmax():
	global N
	global M
	global lmax_set # maps a distance to a list of lmax matrices at that distance
	global reached

	reached_keys = reached.keys()
	for key in reached_keys:
		key_matrix = cnot_util.int_to_matrix(key, N, M)
		has_higher_neighbor = False
		has_equal_neighbor = False
		for i in range(1, M + 1):
			for j in range(1, M + 1):
				if i == j:
					continue

				cnot_util.operation(key_matrix, i, j)

				neighbor_hash = cnot_util.matrix_to_int(key_matrix)
				if reached[neighbor_hash] > reached[key]:
					has_higher_neighbor = True
				if reached[neighbor_hash] == reached[key]:
					has_equal_neighbor = True

				cnot_util.operation(key_matrix, i, j)

		if (not has_higher_neighbor):
			if not reached[key] in lmax_set:
				lmax_set[reached[key]] = []

			lmax_set[reached[key]].append(reached[key])


def extend(op_list):
	global N
	global M
	global queue
	global reached

	for i in range(1, M + 1):
		for j in range(1, M + 1):
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
			to_append = op_list + [(i, j)]
			to_append_hash = cnot_util.matrix_to_int(cnot_util.perform_ops(cnot_util.identity(N, M), to_append))
			if to_append_hash in reached:
				continue
			queue.append(to_append)

def bfs():
	global queue
	global N
	global M
	global reached
	global distances

	reached = dict({}) # dict mapping a matrix hash to its distance to identity
	distances = dict({}) # dict mapping a distance to the number (or list) of matrices that far from identity

	queue.append([])

	cur_op_length = 0

	while len(queue) > 0:

		cur = queue.popleft()

		if len(cur) > cur_op_length:
			print "\nstarting on " + str(len(cur)) + " operations",
			cur_op_length = len(cur)

			# Hacky fix to kill running
			if distances[cur_op_length - 1] == 0:
				break
			# end hacky fix

		#cur_matrix = cnot_util.perform_ops(cnot_util.identity(N), cur)
		cur_matrix = cnot_util.perform_ops(cnot_util.identity(N, M), cur) # for M total rows, extra are ancilla
		cur_hash = cnot_util.matrix_to_int(cur_matrix)

		if cur_hash in reached:
			continue

		reached[cur_hash] = cur_op_length
		extend(cur)

		if not (cur_op_length in distances):
		#	distances[cur_op_length] = 0
			distances[cur_op_length] = []

		#if cnot_util.isUpperTriangular(cur_matrix):
		#	distances[cur_op_length] = distances[cur_op_length] + 1
		cur_matrix.sort()
		distances[cur_op_length].append(cur_matrix)

def test_revhash():
	for i in range(10000000):
		corresp_matrix = cnot_util.int_to_matrix(i, 5)
		back_hash = cnot_util.matrix_to_int(corresp_matrix)

		if not (back_hash == i):
			return (i, back_hash)

		if i%1000000 == 0:
			print i

	return None


if __name__ == '__main__':
	global queue
	global target
	global N
	global M
	global lmax_set
	
	N = 3
	M = 5
	queue = collections.deque([])
	lmax_set = dict({})

	print "Running search lmax on N = " + str(N) + " and total rows is M = " + str(M)

	bfs()
	find_lmax()

	lmax_keys = lmax_set.keys()
	lmax_keys.sort()

	print
	print "Lmaxes are: "
	for key in lmax_keys:
		print str(key) + ": " + str(len(lmax_set[key]))













