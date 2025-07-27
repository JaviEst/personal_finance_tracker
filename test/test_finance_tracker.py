import os
import json
import tempfile
from datetime import date

import pytest

from app.finance_tracker import FinanceTracker, Transaction


@pytest.fixture
def sample_transaction():
    return Transaction("Groceries", 50.0, "Food", "2024-07-01")


@pytest.fixture
def another_transaction():
    return Transaction("Bus", 20.0, "Other", "2024-07-10")


def test_add_and_get_transaction(sample_transaction):
    ft = FinanceTracker()
    ft.add_transaction(sample_transaction)
    assert ft.get_transaction(0) == sample_transaction
    assert ft.get_transaction(1) is None


def test_get_transactions(sample_transaction, another_transaction):
    ft = FinanceTracker([sample_transaction, another_transaction])
    txns = ft.get_transactions()
    assert len(txns) == 2
    assert txns[0].get_description() == "Groceries"
    assert txns[1].get_description() == "Bus"


def test_summary_by_category(sample_transaction, another_transaction):
    ft = FinanceTracker([sample_transaction, another_transaction])
    summary = ft.summary_by_category(2024, 7)
    assert summary["Food"] == 50.0
    assert summary["Other"] == 20.0
    assert all(cat in summary for cat in Transaction.ALLOWED_CATEGORIES)


def test_summary_by_category_empty_month():
    ft = FinanceTracker()
    summary = ft.summary_by_category(2023, 1)
    assert all(v == 0.0 for v in summary.values())


def test_unique_transaction_dates(sample_transaction, another_transaction):
    ft = FinanceTracker([sample_transaction, another_transaction])
    dates = ft.unique_transaction_dates()
    assert isinstance(dates, set)
    assert date(2024, 7, 1) in dates
    assert date(2024, 7, 10) in dates


def test_save_and_load_transactions(sample_transaction, another_transaction):
    ft = FinanceTracker([sample_transaction, another_transaction])
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "transactions.json")
        ft.save_to_file(filepath)

        assert os.path.exists(filepath)
        with open(filepath) as f:
            data = json.load(f)
            assert len(data) == 2
            assert data[0]["description"] == "Groceries"

        new_ft = FinanceTracker()
        new_ft.load_from_file(filepath)
        txns = new_ft.get_transactions()
        assert len(txns) == 2
        assert txns[0].get_category() == "Food"
        assert txns[1].get_category() == "Other"
