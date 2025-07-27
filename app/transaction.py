from datetime import datetime, date
from typing import Tuple


class Transaction:
    """
    Represents a single financial transaction.
    """

    ALLOWED_CATEGORIES: Tuple[str, ...] = (
        "income",
        "food",
        "rent",
        "utilities",
        "entertainment",
        "other",
    )

    def __init__(self, description: str, amount: float, category: str, date_str: str):
        self.__description = description
        self.__amount = amount
        if not category or category.lower() not in Transaction.ALLOWED_CATEGORIES:
            raise ValueError(
                f"Category must be one of {Transaction.ALLOWED_CATEGORIES}"
            )
        self.__category = category

        try:
            self.__date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")

    def get_description(self) -> str:
        return self.__description

    def get_amount(self) -> float:
        return self.__amount

    def get_category(self) -> str:
        return self.__category

    def get_date(self) -> date:
        return self.__date

    def get_transaction(self) -> dict:
        return {
            "description": self.__description,
            "amount": self.__amount,
            "category": self.__category,
            "date": self.__date,
        }

    def __str__(self) -> str:
        return f"{self.__date} | {self.__category} | {self.__description}: ${self.__amount:.2f}"

    def __repr__(self) -> str:
        return f"Transaction({self.__description!r}, {self.__amount}, {self.__category!r}, {self.__date.isoformat()!r})"

    def __eq__(self, other):
        if not isinstance(other, Transaction):
            return False
        return (
            self.__amount == other.__amount
            and self.__category == other.__category
            and self.__description == other.__description
            and self.__date == other.__date
        )
