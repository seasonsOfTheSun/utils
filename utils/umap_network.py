import umap
import networkx as nx

rndstate = np.random.RandomState(108)
A,_,_ = umap.umap_.fuzzy_simplicial_set(features, 10, rndstate, "euclidean")
G = nx.from_scipy_sparse_matrix(A)
