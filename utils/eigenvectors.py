# Get the random-walk eigenvectors
import networkx as nx
import scipy.sparse
import scipy.sparse.linalg

def rw_eigenvectors(G, nodelist=None):

    if nodelist == None: 
        nodelist = list(G.nodes())

    # why the normalized Laplacian matrix and not the Random Walk
    # Laplacian Matrix, you might ask?
    # read on!
    I = scipy.sparse.eye(len(G.nodes()))
    A = I - nx.normalized_laplacian_matrix(G, nodelist=nodelist)


    # we get the eigenvalues of the gloriously *Hermitian* normalized L. matrix.
    # therefore we can use the much faster eigsh as opposed to eigs
    eigenvalues,eigenvectors = scipy.sparse.linalg.eigsh(A, k = 100)
    eigenvalues  = eigenvalues[::-1]
    eigenvectors = eigenvectors[:,::-1]

    # we can then get the *random walk* L. eigenvectors cann be derived from 
    # normalized Laplacian eigenvectors by degree adjustment.
    D_half = scipy.sparse.diags([np.sqrt(G.degree(i)) for i in nodelist])
    rw_eigenvectors = scipy.sparse.linalg.inv(D_half) * eigenvectors
    return rw_eigenvectors, eigenvalues, nodelist
