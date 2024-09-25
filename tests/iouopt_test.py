import random
import unittest
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Set

from iouopt import Journal


@dataclass
class IOU:
    borrower: int
    lender: int
    amount: int


class JournalTest(unittest.TestCase):
    def test_no_ious(self):
        j = Journal[str]()
        self.assertListEqual([], list(j.simplify()))

    def test_same_party(self):
        j = Journal[str]()
        j.append("A", "A", 1)
        self.assertListEqual([], list(j.simplify()))

    def test_amount_zero(self):
        j = Journal[str]()
        j.append("A", "B", 0)
        self.assertListEqual([], list(j.simplify()))

    def test_net_zero(self):
        j = Journal[str]()
        j.append("A", "B", 1)
        j.append("B", "A", 1)
        self.assertListEqual([], list(j.simplify()))

    def test_negative_amount(self):
        j = Journal[str]()
        with self.assertRaises(AssertionError) as cm:
            j.append("A", "B", -1)
        self.assertEqual("amount < 0", str(cm.exception))

    def test_simplify(self):
        for _ in range(20_000):
            inputs = generate_ious(
                num_ious=random.randint(1, 500),
                num_parties=random.randint(2, 50),
                max_amount=1000,
            )

            j = Journal[int]()
            for iou in inputs:
                j.append(iou.borrower, iou.lender, iou.amount)

            outputs = []
            for borrower, lender, amount in j.simplify():
                outputs.append(IOU(borrower, lender, amount))

            self.check_settled(inputs, outputs)

    def check_settled(self, inputs: List[IOU], outputs: List[IOU]):
        # Calculate input/expected values
        input_flow: Dict[int, int] = defaultdict(int)
        for iou in inputs:
            input_flow[iou.lender] += iou.amount
            input_flow[iou.borrower] -= iou.amount

        # Calculate output/actual values
        output_flow: Dict[int, int] = defaultdict(int)
        output_borrowers: Set[int] = set()
        output_lenders: Set[int] = set()
        for iou in outputs:
            output_flow[iou.lender] += iou.amount
            output_flow[iou.borrower] -= iou.amount
            output_borrowers.add(iou.borrower)
            output_lenders.add(iou.lender)

        # Verify IOUs are settled correctly
        for party in set(input_flow.keys()).union(set(output_flow.keys())):
            self.assertEqual(input_flow[party], output_flow[party])

        # Verify that parties are either payer or payee, not both, in the solution
        self.assertEqual(
            len(output_borrowers) + len(output_lenders),
            len(output_borrowers | output_lenders),
        )


def generate_ious(num_ious: int, num_parties: int, max_amount: int) -> List[IOU]:
    assert num_parties > 1
    parties = list(range(num_parties))

    groups: List[List[int]] = []
    while sum(len(g) for g in groups) < num_ious:
        group = random.sample(parties, random.randint(2, num_parties))
        groups.append(group)

    result: List[IOU] = []
    for group in groups:
        lender = random.choice(group)
        for borrower in group:
            amount = random.randint(1, max_amount)
            result.append(IOU(borrower, lender, amount))

    return result
