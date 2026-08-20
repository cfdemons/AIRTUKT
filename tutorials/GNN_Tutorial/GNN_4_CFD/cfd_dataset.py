import torch
import random
import h5py
import numpy as np
from typing import Optional, Callable, Dict

from .graph import Graph


class Dataset(torch.utils.data.Dataset):
    r"""A base class for representing a Dataset.

    Args:
        path (string): Path to the h5 file.
        transform (callable, optional): A function/transform that takes in a :obj:`graphs4cfd.graph.Graph` object
            and returns a transformed version. The data object will be transformed before every access.
            (default: :obj:`None`)
        training_info (dict, optional): A dictionary containing values of type :obj:`ìnt` for the keys `n_in`,
            `n_out`, `step` and `T`. (default: :obj:`None`)
        idx (int, optional): The index of the simulation to load. If :obj:`None`, then all the simulations are loaded.
            (default: :obj:`None`)
        preload (bool, optional): If :obj:`True`, then the data is loaded in memory. If :obj:`False`, then the data
            is loaded from the h5 file at every access. (default: :obj:`False`)
    """

    def __init__(self,
                 path: str,
                 transform: Optional[Callable] = None,
                 training_info: Optional[Dict] = None,
                 idx: int = None,
                 preload: bool = False):
        self.path = path
        self.transform = transform
        self.training_info = training_info
        self.preload = preload
        if training_info:
            self.training_sequences_length = (
                training_info["n_in"] + training_info["n_out"])*training_info["step"] - (training_info["step"]-1)
            self.training_sequences_T = training_info["T"]
        # Load only the given simulation idx
        if idx is not None:
            if preload == False:
                raise ValueError(
                    'If input argument to Dataset.__init__() idx is not None, then argument preload must be True.')
            h5_file = h5py.File(self.path, "r")
            self.h5_data = torch.tensor(
                np.array(h5_file["data"][idx]), dtype=torch.float32)
            if self.h5_data.ndim == 2:
                self.h5_data = self.h5_data.unsqueeze(0)
            h5_file.close()
        # Load all the simulations
        else:
            if self.preload:
                self.load()
            else:
                self.h5_data = None

    def __len__(self) -> int:
        r"""Return the number of samples in the dataset."""
        if self.h5_data is not None:
            return self.h5_data.shape[0]
        else:
            h5_file = h5py.File(self.path, 'r')
            num_samples = h5_file['data'].shape[0]
            h5_file.close()
            return num_samples

    def summary(self):
        """Prints a detailed readout of the dataset structure."""
        with h5py.File(self.path, 'r') as f:
            data_shape = f['data'].shape
            
        print("-" * 30)
        print(f"DATASET STRUCTURE: {self.__class__.__name__}")
        print("-" * 30)
        print(f"File Path:       {self.path}")
        print(f"Total Samples:   {data_shape[0]}")
        print(f"Nodes per Mesh:  {data_shape[1]}")
        print(f"Features/Time:   {data_shape[2]}")
        print(f"Preloaded:       {self.preload}")
        
        if self.training_info:
            print("\nTRAINING CONFIGURATION:")
            for k, v in self.training_info.items():
                print(f"  {k:12}: {v}")
            print(f"  Seq Length:   {self.training_sequences_length} (total steps needed)")
        print("-" * 30)

    def __repr__(self):
        return f"<{self.__class__.__name__} (samples={self.__len__()}, path={self.path})>"

    def __getitem__(self,
                    idx: int) -> Graph:
        r"""Get the idx-th training sequence."""
        sequence_start = random.randint(0, self.training_sequences_T - self.training_sequences_length)
        return self.get_sequence(idx, sequence_start, n_in=self.training_info["n_in"], n_out=self.training_info["n_out"], step=self.training_info["step"])

    def get_sequence(self, 
                     idx: int,
                     sequence_start: Optional[int] = 0,
                     n_in: Optional[int] = 1,
                     n_out: Optional[int] = 1,
                     step: Optional[int] = 1) -> Graph:
        r"""Get the idx-th sequence.

        Args:
            idx (int): The index of the sample.
            sequence_start (int, optional): The starting index of the sequence. (default: :obj:`0`)
            n_in (int, optional): The number of input time-steps. (default: :obj:`1`)
            n_out (int, optional): The number of output time-steps. (default: :obj:`1`)
            step (int, optional): The step between two consecutive time-steps. (default: :obj:`1`)

        Returns:
            :obj:`graphs4cfd.graph.Graph`: The graph containing the sequence.
        """
        # Load the data
        if self.preload:
            data = self.h5_data[idx]
        else:
            h5_file = h5py.File(self.path, 'r')
            data = torch.tensor(h5_file['data'][idx], dtype=torch.float32)
            h5_file.close()
        # Compute the indices
        sequence_length = (n_in + n_out)*step - (step-1)
        idx0 = sequence_start
        idx1 = sequence_start + n_in*step
        idx2 = sequence_start + sequence_length
        # Create graph (only cloud of points)
        graph = self.data2graph(data, idx0, idx1, idx2, step)
        # Apply the transformations
        if self.transform:
            self.transform(graph)
        return graph

    def load(self):
        r"""Load the dataset in memory."""
        print("Loading dataset:", self.path)
        h5_file = h5py.File(self.path, "r")
        self.h5_data = torch.tensor(
            np.array(h5_file["data"]), dtype=torch.float32)
        h5_file.close()
        self.preload = True

    def data2graph(self,
                   data: torch.Tensor,
                   idx0: int,
                   idx1: int,
                   idx2: int,
                   step: int):
        r"""Convert the data to a :obj:`graphs4cfd.graph.Graph` object."""
        graph = Graph()
        return graph



class NsEllipse(Dataset):
    r"""Dataset for the incompressible flow around a circular cylinder. The data is available at [https://doi.org/10.5281/zenodo.7870707](https://doi.org/10.5281/zenodo.7870707).

    Args:
        format (string): The format of the fields, either 'uvp' or 'uv'.
        path (string): Path to the h5 file.
        transform (callable, optional): A function/transform that takes in a :obj:`graphs4cfd.graph.Graph` object
            and returns a transformed version. The data object will be transformed before every access.
            (default: :obj:`None`)
        training_info (dict, optional): A dictionary containing values of type :obj:`ìnt` for the keys `n_in`,
            `n_out`, `step` and `T`. (default: :obj:`None`)
        idx (int, optional): The index of the simulation to load. If :obj:`None`, then all the simulations are loaded.
            (default: :obj:`None`)
        preload (bool, optional): If :obj:`True`, then the data is loaded in memory. If :obj:`False`, then the data
            is loaded from the h5 file at every access. (default: :obj:`True`)
    """

    def __init__(self, format: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert format in ["uv", "uvp"], f"Format {format} not supported, use 'uv' or 'uvp'"
        self.format = format

    def summary(self):
        """Extended summary explaining the CFD-specific data mapping."""
        super().summary()
        print("\nDATA MAPPING (NsCircle):")
        print("  Cols [0:2]:    Position (x, y)")
        print("  Col  [2]:      Global Parameter (Re)")
        print("  Col  [3]:      Boundary Condition ID")
        
        field_type = "u, v, p" if self.format == "uvp" else "u, v"
        print(f"  Cols [4:]:     Field Data ({field_type}) interleaved over time")
        
        if self.training_info:
            n_in, n_out = self.training_info['n_in'], self.training_info['n_out']
            total_channels = 3 if self.format == "uvp" else 2
            print(f"\nGRAPH OUTPUT STRUCTURE:")
            print(f"  Input Channels:  {n_in * total_channels} ({n_in} steps * {total_channels} vars)")
            print(f"  Target Channels: {n_out * total_channels} ({n_out} steps * {total_channels} vars)")
        print("-" * 30)

    def data2graph(self,
                   data: torch.Tensor,
                   idx0: int,
                   idx1: int,
                   idx2: int,
                   step: int) -> Graph:
        r"""Convert the data to a :obj:`graphs4cfd.graph.Graph` object.
        
        Args:
            data (torch.Tensor): The data.
            idx0 (int): The starting index of the sequence.
            idx1 (int): The ending index of the input sequence.
            idx2 (int): The ending index of the sequence.
            step (int): The step between two consecutive time-steps.        
        
        Returns:
            :obj:`graphs4cfd.graph.Graph`: The graph containing the sequence.            
        """
        # Check number of nodes (not np.nan)
        N = (data[:, 0] == data[:, 0]).sum()
        # Remove np.nan and only keep the real nodes
        data = data[:N]
        # Build graph
        graph = Graph()
        graph.pos = data[:, :2] # x, y
        graph.glob = data[:, 2:3] # Re
        if self.format == 'uvp':
            graph.field  = data[:, 4:].reshape(N, -1, 3)[:, idx0:idx1:step, :].reshape(N, -1) # u0, v0, p0, ...
            graph.target = data[:, 4:].reshape(N, -1, 3)[:, idx1:idx2:step, :].reshape(N, -1) # un, vn, pn, ...
        elif self.format == 'uv':
            graph.field  = data[:, 4:].reshape(N, -1, 3)[:, idx0:idx1:step, 0:2].reshape(N, -1) # u0, v0, ...
            graph.target  = data[:, 4:].reshape(N, -1, 3)[:, idx1:idx2:step, 0:2].reshape(N, -1) # un, vn, ...
        # BCs
        '''
        In data[:,3]:
            0 -> Inner flow
            1 -> Periodic boundary
            2 -> Inlet
            3 -> Outlet
            4 -> Wall
        '''
        graph.bound = data[:, 3].type(torch.uint8)
        graph.omega = torch.zeros(N, 1)
        graph.omega[(graph.bound == 2)+(graph.bound == 4), 0] = 1 # Inlet and Wall
        return graph
