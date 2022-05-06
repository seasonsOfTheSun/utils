import numpy as np
import numpy.linalg
import copy

def rescale(x):
  return x/np.maximum(np.max(x, axis=0), -np.min(x, axis=0))

import copy
class Chart:

  def __init__(self,
               network,
               nodelist,
               eigenvector_data,
               n_bins = 30,
               threshold=0.2,
               initial_eigenvector=1
               ):
    
    """
    An object that describes a subset of nodes in the network and eigenvectors 
    that describe them.

    Arguments:
    ---------
    eigenvector_data:
        The dataframe of 

    n_bins:

    threshold:

    initial_eigenvector:
    
    """
    self.network = network
    self.nodelist = nodelist
    self.eigenvector_data = eigenvector_data
    self.n_samples = eigenvector_data.shape[0]
    self.n_bins = n_bins
    self._selected_eigenvectors = np.array([initial_eigenvector])
    self._bins = np.array([(i,) for i in range(n_bins)])
    self.threshold = threshold

  def in_selected_bin(self, selected_bin):
    """Creates a 1d-numpy array with length equal to n_samples
    with value True when the data point is in selected_bin 
    and False elsewhere."""
    out = np.array([True]*self.n_samples)
    bins = np.linspace(0,1,self.n_bins)[1:]
    for e,i in zip(self._selected_eigenvectors, selected_bin):
      #bins = np.quantile(self.eigenvector_data[:,e],np.linspace(0,1,self.n_bins)[1:])
      out &= np.array(np.digitize(self.eigenvector_data[:,e], bins) == i)
    return out

  def std_of_eigenvector_on_bin(self, eigenvector, bin):
    """ 
    Get the standard deviation of of an 
    eigenvector on a selected set of samples.
    """
    return np.std(self.eigenvector_data[self.in_selected_bin(bin), eigenvector])

  def extra_covariance_of_eigenvector_on_bin(self, eigenvector, bin):
    """
    Measures the degree of dependence of eigenvector on the chart within a given bin,.
    """

    select = self.in_selected_bin(bin)

    if select.any() == False:
      # No samples in this bin.
      return np.nan

    if len(self._selected_eigenvectors) > 1:
      # 
      X = self.eigenvector_data[select,:][:,self._selected_eigenvectors]
      Y = self.eigenvector_data[select,:][:,list(self._selected_eigenvectors) + [eigenvector]]
      return np.std(np.linalg.det(np.cov(Y.T))/np.linalg.det(np.cov(X.T)))

    elif len(self._selected_eigenvectors) == 1:
      # 
      Y = self.eigenvector_data[select,:][:, list(self._selected_eigenvectors) + [eigenvector]]
      sigma_2 = np.var(self.eigenvector_data[select,:][:,self._selected_eigenvectors])
      return np.std(np.linalg.det(np.cov(Y.T))/sigma_2)

  def domain_of_new_parameter(self, eigenvector):
    """
    Return the indices of all the bins where 
    std of eigenvector is above some threshold."""
    return [self.std_of_eigenvector_on_bin(eigenvector,bin) > self.threshold 
            for bin in self._bins]

  def extend_bins(self, selected_bins):
    # Return the bins in the chart, extended with all 
    # possible bins in the new dimension.
    out = []
    for i in selected_bins:
      for j in range(self.n_bins):
        out.append(list(i)+[j])
    return np.array(out)

  def extend_to_new_chart(self, new_eigenvector):
    # creates a new chart with a
    # new eigenvector as a parameter
    # and with bins given where the
    # new thing is well defined.

    out = copy.copy(self)
    out._selected_eigenvectors = np.array(list(self._selected_eigenvectors)+[new_eigenvector])
    selected_bins = self.domain_of_new_parameter(new_eigenvector)
    out._bins = self.extend_bins(self._bins[selected_bins])
    return out

  def get_connected_blocks(G, nodelist, arr_):
    """
    Given a array arr_ of booleans,
    return a list of lists, where each sublist
    gives the indices for a component of the graph.
    """
    out = []
    for component in nx.connected_components(G.subgraph(np.array(nodelist)[arr_])):
        out.append(np.array([i in component for i in nodelist]))
    return out

  def test_eigenvector(self, eigenvector):
    above_threshold = [self.extra_covariance_of_eigenvector_on_bin(eigenvector, bin) > self.threshold
                       for bin in self._bins]
    return sum(above_threshold) > 0.5*self.n_bins

