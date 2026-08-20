import torch
import torch.nn.functional as F
from torch import nn
from typing import Optional, Dict, List
import re

from .model import GNN
from .blocks import MLP, MP, DownMP, UpMP
from ..graph import Graph


class UniversalGNN(GNN):
    """
    Universal GNN matching mus_gnn.py conventions exactly.
    Supports 1-N scales with DownMP/UpMP transitions.
    """

    def __init__(self, arch: Dict = None, *args, **kwargs):
        super().__init__(arch=arch, *args, **kwargs)

    def load_arch(self, arch: Dict):
        self.arch = arch
        self.mp_blocks   = nn.ModuleDict()
        self.down_blocks = nn.ModuleDict()
        self.up_blocks   = nn.ModuleDict()
        self.encoders    = nn.ModuleDict()

        # --- Encoders ---
        if "edge_encoder" in arch:
            self.encoders["edge_encoder"] = MLP(*arch["edge_encoder"])
        if "node_encoder" in arch:
            self.encoders["node_encoder"] = MLP(*arch["node_encoder"])

        # --- MP blocks: keys matching mp<digits> only ---
        mp_re   = re.compile(r"^mp\d+$")
        down_re = re.compile(r"^down_mp(\d)(\d)$")
        up_re   = re.compile(r"^up_mp(\d)(\d)$")

        for key, val in arch.items():
            if mp_re.match(key):
                self.mp_blocks[key] = MP(*val)
            elif down_re.match(key):
                # val is a single 3-tuple (in, hidden_dims, act)
                # DownMP takes (mlp_spec, level_index)
                from_scale = int(down_re.match(key).group(1))
                self.down_blocks[key] = DownMP(val, from_scale)
            elif up_re.match(key):
                from_scale = int(up_re.match(key).group(1))
                self.up_blocks[key] = UpMP(val, from_scale)

        if "decoder" in arch:
            self.node_decoder = MLP(*arch["decoder"])

        # Detect number of scales from down_mp keys
        down_keys = [k for k in arch if down_re.match(k)]
        self.num_scales = len(down_keys) + 1  # e.g. 1 down_mp → 2 scales

        self.to(self.device)

    def _mp_keys_sorted(self, prefix: str) -> List[str]:
        """Return MP block keys starting with `prefix`, sorted by trailing block number."""
        keys = [k for k in self.mp_blocks if k.startswith(prefix)]
        return sorted(keys, key=lambda k: int(k[len(prefix):]))

    def forward(self, graph: Graph, t: Optional[int] = None):
        # Save originals for restoration
        orig_field     = graph.field
        orig_edge_attr = graph.edge_attr

        # --- Concatenate node features ---
        graph.field = torch.cat(
            [getattr(graph, v) for v in ('field', 'loc', 'glob', 'omega') if hasattr(graph, v)],
            dim=1
        )

        # --- Encode ---
        graph.edge_attr = F.selu(self.encoders["edge_encoder"](graph.edge_attr))
        graph.field     = F.selu(self.encoders["node_encoder"](graph.field))

        # --- Down pass ---
        # skip_states[scale] = (field, pos, edge_index, edge_attr)  — exactly as in mus_gnn
        skip_states = {}

        for s in range(1, self.num_scales):      # scales 1 .. num_scales-1
            # Run down-path MP blocks: prefix mp{s}1
            keys = self._mp_keys_sorted(f"mp{s}1")
            for key in keys:
                graph.field, graph.edge_attr = self.mp_blocks[key](
                    graph.field, graph.edge_attr, graph.edge_index
                )
                graph.field, graph.edge_attr = F.selu(graph.field), F.selu(graph.edge_attr)

            # Save skip state (field, pos, edge_index, edge_attr) — no batch needed
            skip_states[s] = (graph.field, graph.pos, graph.edge_index, graph.edge_attr)

            # Downsample
            graph = self.down_blocks[f"down_mp{s}{s+1}"](graph, activation=torch.tanh)

        # --- Bottleneck ---
        bot = self.num_scales
        bot_keys = self._mp_keys_sorted(f"mp{bot}")
        for i, key in enumerate(bot_keys):
            last = (i == len(bot_keys) - 1)
            if last:
                graph.field, _ = self.mp_blocks[key](graph.field, graph.edge_attr, graph.edge_index)
                graph.field    = F.selu(graph.field)
            else:
                graph.field, graph.edge_attr = self.mp_blocks[key](
                    graph.field, graph.edge_attr, graph.edge_index
                )
                graph.field, graph.edge_attr = F.selu(graph.field), F.selu(graph.edge_attr)

        # --- Up pass ---
        for s in range(self.num_scales - 1, 0, -1):  # scales num_scales-1 .. 1
            field_skip, pos_skip, ei_skip, ea_skip = skip_states[s]

            # Upsample (UpMP internally handles knn + cat with skip)
            graph = self.up_blocks[f"up_mp{s+1}{s}"](graph, field_skip, pos_skip, activation=torch.tanh)

            # Manually restore edge topology — exactly as in mus_gnn.py
            graph.edge_index, graph.edge_attr = ei_skip, ea_skip

            # Run up-path MP blocks: prefix mp{s}2
            up_keys = self._mp_keys_sorted(f"mp{s}2")
            for i, key in enumerate(up_keys):
                last = (i == len(up_keys) - 1)
                if last:
                    graph.field, _ = self.mp_blocks[key](graph.field, graph.edge_attr, graph.edge_index)
                    graph.field    = F.selu(graph.field)
                else:
                    graph.field, graph.edge_attr = self.mp_blocks[key](
                        graph.field, graph.edge_attr, graph.edge_index
                    )
                    graph.field, graph.edge_attr = F.selu(graph.field), F.selu(graph.edge_attr)

        # --- Decode ---
        output = self.node_decoder(graph.field)

        # --- Restore ---
        graph.field, graph.edge_attr = orig_field, orig_edge_attr

        return graph.field[:, -self.num_fields:] + output
