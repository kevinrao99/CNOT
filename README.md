# CNOT
for things related to complexity of linear functions

cnot_lmax_searcher: visits all N x M matrices (M = N for no aniclla) and finds the local maximums

cnot_mim_lmax_searcher: uses meet-in-middle to find the complexity of a particular matrix and tests if it's a local maximum

cnot_mim_searcher: uses meet-in-middle to find the complexity of a particular matrix

cnot_pmp_visit_allmat: visits all matrices by BFSing and also marking all PMP^-1 equivalent matrices as visited

cnot_util: contains commonly used functions like constructing an identity or applying an operation to a matrix

cnot_visit_allmat: visits all matrices with BFS
