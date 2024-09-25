from collections import defaultdict
from typing import Dict, Generic, Hashable, Iterator, List, Tuple, TypeVar

import numpy as np

from iouopt.flow import min_cost_flow

N = TypeVar("N", bound=Hashable)


class Journal(Generic[N]):
    def __init__(self):
        self.nodes: Dict[N, int] = defaultdict(int)

    def append(self, borrower: N, lender: N, amount: int):
        assert amount >= 0, "amount < 0"
        self.nodes[lender] -= amount
        self.nodes[borrower] += amount

    def simplify(self) -> Iterator[Tuple[N, N, int]]:
        if len(self.nodes) < 2:
            return

        nodes: List[N] = []
        demand = np.zeros(len(self.nodes), dtype=np.int64)
        for i, (node, d) in enumerate(self.nodes.items()):
            nodes.append(node)
            demand[i] = d

        for u, v, amount in min_cost_flow(demand):
            yield nodes[u], nodes[v], amount
