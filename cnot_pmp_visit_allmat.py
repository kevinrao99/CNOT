import collections
import cnot_util

class PMP_class:

	def __init__(self, representative, distance):
		self.rep = representative
		self.dist = distance
		self.members = set()
		self.adjacent = []

	def __lt__(self, other):
         return self.dist < other.dist

	def __str__(self):
		output = ""
		output = output + "\nRep for class of distance " + str(self.dist) + " with " + str(len(self.members)) + " members:\n"
		for arr in self.rep:
			output = output + str(arr) + "\n"

		output = output + "Adjacent distances:\n"
		for adj in self.adjacent:
			output = output + str(adj.dist) + " "
			'''
			for arr in adj.rep:
				output = output + str(arr) + "\n"
			ourput = output + "\n \n"
			'''
		output = output + "\n"
		'''
		output = output + "\nMembers:\n"
		for member in self.members:
			member_mat = cnot_util.int_to_matrix(member, len(self.rep), len(self.rep[0]))
			for arr in member_mat:
				output = output + str(arr) + "\n"
			output = output + "\n"
		'''

		return output


def transpose(matrix):
	# outputs a new matrix without modifying original, which is transpose of original
	global N
	global M

	if not (N == M):
		print "====== ERROR not transposing a square matrix ======"
		return

	ans = []
	for i in range(N):
		ans.append([])
		for j in range(N):
			ans[i].append(matrix[j][i])

	return ans

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
	global include_transpose

	cur_hash = cnot_util.matrix_to_int(matrix)
	cur_distance = reached[cur_hash]

	if cur_hash in matrix_to_pmp: # If we've already processed the equiv class of this matrix, don't do it again
		return

	cur_pmp = PMP_class(matrix, cur_distance)
	pmp_to_matrix[cur_pmp] = matrix

	perm = range(N)

	def process_equiv_relation(relation, matrix):
		# given a relation which on input the original matrix outputs a matrix in the equivalence class defined by the relation, processes the relation on the matrix
		# for example, given a permutation an matrix, processes pmp
		# the relation parameter is a function

		equiv_matrix = relation(matrix)
		equiv_hash = cnot_util.matrix_to_int(equiv_matrix)

		cur_pmp.members.add(equiv_hash)
		matrix_to_pmp[equiv_hash] = cur_pmp

		'''
		if not (equiv_hash in reached):
			reached[equiv_hash] = cur_distance
			distances[cur_distance].append(equiv_matrix)
		''' # Optimization to avoid visiting matrices multiple times, but this only works if the equivalence relation is vertex transitive

		return equiv_matrix

	while perm: # quits when perm is None

		# apply PMP^-1, hash result with matrix_to_int, store in reached and distances
		# Then do transpose of the PMP, same thing

		perm_matrix = process_equiv_relation(lambda matrix: perm_as_pmp(perm, matrix), matrix)

		if include_transpose:
			process_equiv_relation(lambda matrix: transpose(matrix), perm_matrix)

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
			print "starting on " + str(len(cur)) + " operations"
			cur_op_length = len(cur)

		if len(cur) < cur_op_length:
			print "Shouldn't be here due to BFS invariant"
			return

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

	for i in range(1, N + 1):
		for j in range(1, N + 1):
			if i == j:
				continue

			cnot_util.operation(class_rep, i, j)
			if cnot_util.matrix_to_int(class_rep) in pmp_2.members:
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
	global include_transpose

	N = 3
	M = N
	include_transpose = True and (M == N)


	queue = collections.deque([])

	print "Running search of all matrices with PMP^-1 for N = " + str(N)
	if include_transpose:
		print "Including transpose in equiv class"
	else:
		print "Not including transpose in equiv class"

	bfs()
	build_pmp_graph()

	dist_keys = distances.keys()
	dist_keys.sort()

	print
	print "Matrix distances:"
	for key in dist_keys:
		print str(key) + ": " + str(len(distances[key]))

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

	print

	'''
	print "class representatives:"
	for key in pmp_keys:
		print key.dist
		for arr in key.rep:
			print arr
	
	'''


	pmp_keys.sort()
	for key in pmp_keys:
		print key





