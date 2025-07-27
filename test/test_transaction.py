import pytest
from datetime import date

from app.transaction import Transaction


def test_transaction_creation():
    txn = Transaction("Salary", 5000.0, "income", "2025-07-01")
    assert txn.get_description() == "Salary"
    assert txn.get_amount() == 5000.0
    assert txn.get_category() == "income"
    assert txn.get_date() == date(2025, 7, 1)
    assert txn.get_transaction() == {
        "description": "Salary",
        "amount": 5000.0,
        "category": "income",
        "date": date(2025, 7, 1),
    }


@pytest.mark.parametrize("invalid_category", ["invalid", "", "travel", None])
def test_transaction_invalid_category(invalid_category):
    with pytest.raises(ValueError, match=r"Category must be one of .*"):
        Transaction("Groceries", 100.0, invalid_category, "2025-07-01")


@pytest.mark.parametrize(
    "invalid_date", ["2025/07/01", "July 1, 2025", "", "2025-13-01"]
)
def test_transaction_invalid_date_format(invalid_date):
    with pytest.raises(ValueError, match="Date must be in YYYY-MM-DD format"):
        Transaction("Rent", 1200.0, "rent", invalid_date)


def test_transaction_str_repr_eq():
    txn1 = Transaction("Movie", 15.0, "entertainment", "2025-07-01")
    txn2 = Transaction("Movie", 15.0, "entertainment", "2025-07-01")
    txn3 = Transaction("Dinner", 30.0, "food", "2025-07-01")

    # __str__
    assert str(txn1) == "2025-07-01 | entertainment | Movie: $15.00"

    # __repr__
    assert repr(txn1) == "Transaction('Movie', 15.0, 'entertainment', '2025-07-01')"

    # __eq__ positive and negative cases
    assert txn1 == txn2
    assert txn1 != txn3
    assert txn1 != "NotATransaction"
