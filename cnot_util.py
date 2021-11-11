


def identity(N = 4):
	ans = []
	for i in range(N):
		new_row = []
		for j in range(N):
			if j == i:
				new_row.append(1)
			else:
				new_row.append(0)
		ans.append(new_row)
	return ans

def identity(N, M):
	#returns an identity for NxN but total M rows, with extra are ancilla
	ans = []
	for i in range(M):
		new_row = []
		for j in range(N):
			if j == i:
				new_row.append(1)
			else:
				new_row.append(0)
		ans.append(new_row)
	return ans


def matrix_to_int(matrix):
	exponent = 0
	tot = 0
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			tot += (2 ** exponent) * matrix[i][j]
			exponent += 1

	return tot

def int_to_matrix(matrix_hash, N, M):
	# inverts the hash for an N x N matrix with M total rows (ancilla)

	ans = []
	for i in range(M):
		new_row = []
		for j in range(N):
			new_row.append(0)
		ans.append(new_row)

	hash_copy = matrix_hash

	for i in range(len(ans)):
		for j in range(len(ans[i])):
			ans[i][j] = hash_copy % 2
			hash_copy = hash_copy // 2

	return ans


def next_permutation(perm):
	# returns the next permutation in alphabetical order and computes it in place (destructively)
	# if we're at the max permutation, return None
	# Assumes perm is a 1 dimensional array of consecutive integers

	first_lower_index = -1

	for i in range(len(perm) - 1):
		j = len(perm) - i - 2 # so we iterate from the back of the array
		if perm[j] < perm[j + 1]:
			first_lower_index = j
			break

	if first_lower_index == -1:
		return None

	one_higher_index = -1

	for i in range(first_lower_index, len(perm)):
		if perm[first_lower_index] < perm[i]:
			if perm[i] < perm[one_higher_index] or one_higher_index == -1:
				one_higher_index = i

	temp = perm[one_higher_index]
	perm[one_higher_index] = perm[first_lower_index]
	perm[first_lower_index] = temp

	perm[first_lower_index + 1:] = sorted(perm[first_lower_index + 1:])

	return perm


def isUpperTriangular(matrix):

	if not (len(matrix) == len(matrix[0])):
		return False

	for i in range(len(matrix)):
		if not (matrix[i][i] == 1):
			return False

	for i in range(len(matrix)):
		for j in range(i):
			if not (matrix[i][j] == 0):
				return False

	return True

def perform_ops(starting, op_list):
	# returns the starting matrix with the specified operations done on it
	# starting should be identity in this case

	for (a, b) in op_list:
		operation(starting, a, b)

	return starting

def operation(matrix, a, b):
	# in NxN matrix, destructively add row a to row b

	a_index = a - 1
	b_index = b - 1

	for i in range(len(matrix[a_index])):
		matrix[b_index][i] = (matrix[a_index][i] + matrix[b_index][i]) % 2

	return

def matrix_equals(matrix_a, matrix_b):
	# returns true iff matrix_a and matrix_b are equal

	for i in range(len(matrix_a)):
		for j in range(len(matrix_a[i])):
			if not (matrix_a[i][j] == matrix_b[i][j]):
				return False

	return True
