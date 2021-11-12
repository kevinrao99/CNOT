import collections
import cnot_util

def extend(op_list):
	global N
	global queue
	global reached

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
			to_append = op_list + [(i, j)]
			to_append_hash = cnot_util.matrix_to_int(cnot_util.perform_ops(cnot_util.identity(N, N), to_append))
			if to_append_hash in reached:
				continue
			queue.append(to_append)

def bfs():
	global queue
	global N
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

		cur_matrix = cnot_util.perform_ops(cnot_util.identity(N, N), cur)
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
		
		distances[cur_op_length].append(cur_matrix)



if __name__ == '__main__':
	global queue
	global target
	global N
	global distances
	

	N = 3
	queue = collections.deque([])

	print "Running visit allmat on N = " + str(N)

	bfs()

	dist_keys = distances.keys()
	dist_keys.sort()

	print
	for key in dist_keys:
		print str(key) + ": " + str(len(distances[key]))

	'''
	for key in dist_keys:
		for mat in distances[key]:
			for i in range(len(mat)):
				for j in mat[i]:
					print str(j) + " ",
				print
			print
	
	'''
	distances[2] = sorted(distances[2])

	for matrix in distances[2]:
		for i in range(len(matrix)):
			print matrix[i]
		print



	
