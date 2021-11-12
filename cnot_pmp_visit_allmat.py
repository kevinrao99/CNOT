import collections
import cnot_util

class PMP_class:

	def __init__(self, representative, distance):
		self.rep = representative
		self.dist = distance
		self.members = []
		self.adjacent = []



def perm_as_pmp(perm, matrix):
	# constructs a new matrix without modifying the original, outputs PMP^-1
	global N

	ans = []

	# row i in answer is row perm[i] in matrix
	for i in range(N):
		ans.append([])
		for j in range(N):
			ans[i].append(matrix[perm[i]][perm[j]])

	return ans

def visit_equiv_matrices(matrix):
	# makes a pmp class
	# Goes through all permutations, does PMP^-1, marks the result as visited and adds it to the pmp class
	global N
	global distances
	global reached
	global pmp_to_matrix
	global matrix_to_pmp

	cur_hash = cnot_util.matrix_to_int(matrix)
	cur_distance = reached[cur_hash]

	cur_pmp = PMP_class(matrix, cur_distance)
	pmp_to_matrix[cur_pmp] = matrix

	perm = range(N)

	while perm: # quits when perm is None

		# apply PMP^-1, hash result with matrix_to_int, store in reached and distances

		permuted_matrix = perm_as_pmp(perm, matrix)
		permuted_hash = cnot_util.matrix_to_int(permuted_matrix)

		cur_pmp.members.append(permuted_matrix)
		matrix_to_pmp[permuted_hash] = cur_pmp

		if not (permuted_hash in reached):
			reached[permuted_hash] = cur_distance

			if not (cur_distance in distances):
				print "shouldn't ever be here in visit_equiv_matrices"
				distances[cur_distance] = []

			distances[cur_distance].append(permuted_matrix)

		perm = cnot_util.next_permutation(perm)

	return None

def extend(op_list):
	global N
	global M
	global queue
	global reached
	global pmp_to_matrix
	global matrix_to_pmp

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

				'''
				if not (i == a) and not (i == b) and not (j == a):
					if i > a:
						continue
				elif i == a:
					if j >= b:
						continue
				'''

				if i == a and j == b:
					continue # Temporarily removes some optimization for testing

				

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

	global pmp_to_matrix
	global matrix_to_pmp

	reached = dict({}) # dict mapping a matrix hash to its distance to identity
	distances = dict({}) # dict mapping a distance to the number (or list) of matrices that far from identity
	pmp_to_matrix = dict({}) # maps a pmp class to its representative
	matrix_to_pmp = dict({}) # maps a matrix hash to its pmp class

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

		distances[cur_op_length].append(cur_matrix)

		visit_equiv_matrices(cur_matrix)

def pmp_adjacent(pmp_1, pmp_2):
	global N
	global pmp_to_matrix
	global matrix_to_pmp

	class_rep = pmp_1.rep

	for i in range(N + 1):
		for j in range(N + 1):
			if i == j:
				continue

			cnot_util.operation(class_rep, i, j)
			if class_rep in pmp_2.members:
				cnot_util.operation(class_rep, i, j)
				return True
			else:
				cnot_util.operation(class_rep, i, j)

	return False


def build_pmp_graph():
	global N
	global pmp_to_matrix
	global matrix_to_pmp

	classes = pmp_to_matrix.keys()

	for pmp_class in classes:
		for other_class in classes:
			if pmp_class == other_class:
				continue

			if pmp_adjacent(pmp_class, other_class):
				pmp_class.adjacent.append(other_class)





if __name__ == "__main__":
	global N
	global M # total rows, extra are ancilla
	global queue

	N = 4
	M = N


	queue = collections.deque([])

	print "Running search of all matrices with PMP^-1 for N = " + str(N)

	bfs()

	dist_keys = distances.keys()
	dist_keys.sort()

	print
	print "Matrix distances:"
	for key in dist_keys:
		print str(key) + ": " + str(len(distances[key]))

	distances[2] = sorted(distances[2])

	'''
	for matrix in distances[2]:
		for i in range(len(matrix)):
			print matrix[i]
		print
	'''

	print
	pmp_keys = pmp_to_matrix.keys()
	dist_ct = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for key in pmp_keys:
		dist_ct[key.dist] += 1

	print "equiv classes distances:"
	for i in range(len(dist_ct)):
		if dist_ct[i] == 0:
			continue
		print str(i) + ": " + str(dist_ct[i])







