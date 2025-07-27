import sys

from app.transaction import Transaction
from app.finance_tracker import FinanceTracker


def prompt_transaction() -> Transaction:
    description = input("Enter description: ")
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount. Must be a number.")
        return None

    category = input(f"Enter category {Transaction.ALLOWED_CATEGORIES}: ").lower()
    date_str = input("Enter date (YYYY-MM-DD): ")

    try:
        return Transaction(description, amount, category, date_str)
    except ValueError as e:
        print(f"Error: {e}")
        return None


def main():
    tracker = FinanceTracker()

    while True:
        print("\n--- Personal Finance Tracker ---")
        print("1. Add transaction")
        print("2. View all transactions")
        print("3. View monthly summary by category")
        print("4. Save to file")
        print("5. Load from file")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            txn = prompt_transaction()
            if txn:
                tracker.add_transaction(txn)
                print("Transaction added.")
        elif choice == "2":
            transactions = tracker.get_transactions()
            if not transactions:
                print("No transactions recorded.")
            else:
                for t in transactions:
                    print(t)
        elif choice == "3":
            try:
                year = int(input("Enter year (YYYY): "))
                month = int(input("Enter month (1-12): "))
            except ValueError:
                print("Invalid input for year or month.")
            else:
                summary = tracker.summary_by_category(year, month)
                print("\nCategory Summary:")
                for category, amount in summary.items():
                    print(f"{category.capitalize()}: ${amount:.2f}")
        elif choice == "4":
            filepath = input("Enter filename to save to (e.g., data.json): ")
            try:
                tracker.save_to_file(filepath)
                print(f"Data saved to {filepath}")
            except Exception as e:
                print(f"Error saving file: {e}")
        elif choice == "5":
            filepath = input("Enter filename to load from (e.g., data.json): ")
            try:
                tracker.load_from_file(filepath)
                print(f"Data loaded from {filepath}")
            except Exception as e:
                print(f"Error loading file: {e}")
        elif choice == "6":
            print("Exiting... Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please choose a number from 1 to 6.")


if __name__ == "__main__":
    main()
