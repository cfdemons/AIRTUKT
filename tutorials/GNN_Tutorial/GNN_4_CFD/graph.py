from torch_geometric.data import Data

# from .plot import ......


class Graph(Data):
    r"""
    A data object describing a graph, extension of the torch_geometric.data.Data but with plotting and tutorial specific methods attached
    """

    def __init__(self, x = None, edge_index = None, edge_attr = None, y = None, pos = None, time = None, **kwargs):
        super().__init__(x, edge_index, edge_attr, y, pos, time, **kwargs)

#    def plot....