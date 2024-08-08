from collections import defaultdict
from itertools import permutations
from typing import Dict, Generic, Hashable, Iterator, Set, Tuple, TypeVar

import networkx as nx  # type: ignore

T = TypeVar("T", bound=Hashable)


class Journal(Generic[T]):
    def __init__(self, strict: bool = False):
        self.nodes: Dict[T, int] = defaultdict(int)
        self.edges: Set[Tuple[T, T]] = set()
        self.strict: bool = strict

    def append(self, borrower: T, lender: T, amount: int):
        assert amount >= 0, "amount < 0"
        self.nodes[lender] -= amount
        self.nodes[borrower] += amount
        if self.strict and lender != borrower:
            self.edges.add((lender, borrower))

    def simplify(self) -> Iterator[Tuple[T, T, int]]:
        if len(self.nodes) > 0:
            # Build demand graph
            G = nx.DiGraph()
            # Add nodes with `demand` attribute for network simplex
            for u, demand in self.nodes.items():
                G.add_node(u, demand=demand)
            # Add observed edges if strict, else construct a complete graph.
            for u, v in self.edges if self.strict else permutations(self.nodes, 2):
                # Set equal edge weights != 0 as a workaround for this bug:
                # https://github.com/networkx/networkx/issues/7562
                G.add_edge(u, v, weight=1)
            # Let networkx do the heavy lifting
            receivables: Dict[T, Dict[T, int]] = nx.network_simplex(G)[1]
            # Extract relevant (non-zero) edges
            for lender, borrowers in receivables.items():
                for borrower, amount in borrowers.items():
                    if amount != 0:
                        yield borrower, lender, amount
