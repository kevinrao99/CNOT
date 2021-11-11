import collections
import cnot_util

def visit_equiv_matrices(matrix):
	# Goes through all permutations, does PMP^-1, marks the result as visited.
	global N
	global distances
	global reached

	cur_distance = reached[cnot_util.matrix_to_int(matrix)]

	perm = range(N)

	while perm: # quits when perm is None

		# apply PMP^-1, hash result with matrix_to_int, store in reached and distances

		perm = cnot_util.next_permutation(perm)


	return None

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
					continue # Temporarily removes some optimization for testing

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

		cur_matrix = cnot_util.perform_ops(cnot_util.identity(N, M), cur) # for M total rows, extra are ancilla
		cur_hash = cnot_util.matrix_to_int(cur_matrix)

		if cur_hash in reached:
			continue

		reached[cur_hash] = cur_op_length
		extend(cur)

		if not (cur_op_length in distances):
			distances[cur_op_length] = []

		cur_matrix.sort()
		distances[cur_op_length].append(cur_matrix)

		visit_equiv_matrices(cur_matrix)



if __name__ == "__main__":
	global N
	global M # total rows, extra are ancilla

	N = 4
	M = N

	start_perm = range(5)
	for i in range(120):
		print start_perm
		start_perm = cnot_util.next_permutation(start_perm)






