import json
from datetime import datetime
from typing import List, Dict, Set

from app.transaction import Transaction


class FinanceTracker:
    """
    Manages a collection of transactions, provides summaries and I/O.
    """

    def __init__(self, transactions: List[Transaction] = None):
        self.__transactions: List[Transaction] = transactions if transactions else []

    def get_transaction(self, idx) -> Transaction:
        if idx >= len(self.__transactions):
            return None

        return self.__transactions[idx]

    def get_transactions(self) -> List[Transaction]:
        return self.__transactions.copy()

    def add_transaction(self, txn: Transaction) -> None:
        self.__transactions.append(txn)

    def summary_by_category(self, year: int, month: int) -> Dict[str, float]:
        summary: Dict[str, float] = {cat: 0.0 for cat in Transaction.ALLOWED_CATEGORIES}
        for txn in self.__transactions:
            txn_date = txn.get_date()
            if txn_date.year == year and txn_date.month == month:
                if txn.get_category() not in summary:
                    summary[txn.get_category()] = txn.get_amount()
                else:
                    summary[txn.get_category()] += txn.get_amount()

        return summary

    def unique_transaction_dates(self) -> Set[datetime.date]:
        return set(txn.get_date() for txn in self.__transactions)

    def save_to_file(self, filepath: str) -> None:
        data = [
            {
                "description": t.get_description(),
                "amount": t.get_amount(),
                "category": t.get_category(),
                "date": t.get_date().isoformat(),
            }
            for t in self.__transactions
        ]
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def load_from_file(self, filepath: str) -> None:
        with open(filepath, "r") as f:
            data = json.load(f)
        for item in data:
            txn = Transaction(
                item["description"], item["amount"], item["category"], item["date"]
            )
            self.add_transaction(txn)
