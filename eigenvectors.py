# Get the random-walk eigenvectors
import networkx as nx
import scipy.sparse
import scipy.sparse.linalg

nodelist = list(G.nodes())
I = scipy.sparse.eye(len(G.nodes()))
A = I - nx.normalized_laplacian_matrix(G, nodelist=nodelist)
D_half = scipy.sparse.diags([np.sqrt(G.degree(i)) for i in nodelist])
eigenvalues,eigenvectors = scipy.sparse.linalg.eigsh(A, k = 100)
eigenvalues  = eigenvalues[::-1]
eigenvectors = eigenvectors[:,::-1]
rw_eigenvectors = scipy.sparse.linalg.inv(D_half) * eigenvectors