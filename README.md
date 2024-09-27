# iouopt

`iouopt` simplifies group [IOU](https://en.wikipedia.org/wiki/IOU) settlement. If you've used [Splitwise](https://blog.splitwise.com/2012/09/14/debts-made-simple/) or similar apps, you're familiar with the concept.

## Usage

```python
import iouopt import Journal

j = Journal[str]()

j.append(borrower="A", lender="B", amount=5)
j.append("A", "C", 15)
j.append("B", "A", 10)
j.append("B", "C", 5)
j.append("C", "A", 20)
j.append("C", "B", 15)

for borrower, lender, amount in j.simplify():
    print(f"#=> {borrower} pays {lender} {amount}")

#=> C pays A 10
#=> C pays B 5
```

**Note:** `iouopt` requires that all amounts are represented as an `int`. This is a constraint of the underlying minimum-cost flow algorithm. If you need to express partial units, such as 15.78, multiply amounts by a suitable constant factor (e.g., 100) and then convert them to an int.

## Install

Install the latest version from the [Python Package Index (PyPI)](https://pypi.org/project/iouopt/).

```console
$ pip install iouopt
```
