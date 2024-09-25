from typing import Iterator, Tuple

import numpy as np
import numpy.typing as npt
from ortools.graph.python import min_cost_flow as ortmcf  # type: ignore


def min_cost_flow(
    demand: npt.NDArray[np.int64],
) -> Iterator[Tuple[int, int, int]]:
    node_count = demand.shape[0]
    edge_count = node_count * (node_count - 1)

    # Create a complete graph.
    nodes = np.arange(node_count, dtype=np.int32)
    source_grid, target_grid = np.meshgrid(nodes, nodes, indexing="ij")
    mask = source_grid != target_grid
    source = source_grid[mask]
    target = target_grid[mask]

    # Edge capacities are equal and effectively infinite
    capacity = np.full(edge_count, np.abs(demand).sum(), dtype=np.int64)

    # Edge costs are equal and greater than zero to minimize edge count
    cost = np.ones(edge_count, dtype=np.int64)

    # Build the mcf problem
    mcf = ortmcf.SimpleMinCostFlow()
    arcs = mcf.add_arcs_with_capacity_and_unit_cost(source, target, capacity, cost)
    mcf.set_nodes_supplies(nodes, demand)

    # Solve the problem
    status = mcf.solve()
    assert status == mcf.OPTIMAL, status

    # Unpack and yield the solution
    for i, flow in zip(arcs, mcf.flows(arcs)):  # type: ignore
        if flow > 0:
            u = source[i].astype(int)
            v = target[i].astype(int)
            yield u, v, flow  # type: ignore
