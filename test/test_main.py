import main
from app.transaction import Transaction
from app.finance_tracker import FinanceTracker


def test_prompt_transaction_valid(monkeypatch):
    inputs = iter(["Groceries", "45.6", "food", "2023-06-01"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    txn = main.prompt_transaction()
    assert isinstance(txn, Transaction)
    assert txn.get_description() == "Groceries"
    assert txn.get_amount() == 45.6
    assert txn.get_category() == "food"
    assert txn.get_date().strftime("%Y-%m-%d") == "2023-06-01"


def test_prompt_transaction_invalid_amount(monkeypatch, capsys):
    inputs = iter(["Groceries", "not-a-number"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    txn = main.prompt_transaction()
    captured = capsys.readouterr()
    assert txn is None
    assert "Invalid amount" in captured.out


def test_prompt_transaction_invalid_category(monkeypatch, capsys):
    inputs = iter(["Groceries", "10", "invalid-category", "2023-06-01"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    txn = main.prompt_transaction()
    captured = capsys.readouterr()
    assert txn is None
    assert "Category must be one of" in captured.out


def test_prompt_transaction_invalid_date(monkeypatch, capsys):
    inputs = iter(["Groceries", "10", "food", "bad-date"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    txn = main.prompt_transaction()
    captured = capsys.readouterr()
    assert txn is None
    assert "Invalid date format" in captured.out or "Error:" in captured.out


def run_main_with_inputs(monkeypatch, inputs):
    tracker = FinanceTracker()
    monkeypatch.setattr(main, "FinanceTracker", lambda: tracker)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("sys.exit", lambda _: (_ for _ in ()).throw(SystemExit))
    try:
        main.main()
    except SystemExit:
        pass
    return tracker


def test_main_add_view_exit(monkeypatch, capsys):
    inputs = iter(["1", "Groceries", "50", "food", "2023-06-01", "2", "6"])
    _ = run_main_with_inputs(monkeypatch, inputs)
    captured = capsys.readouterr()
    assert "Transaction added." in captured.out
    assert "2023-06-01 | food | Groceries: $50.00" in captured.out


def test_main_view_summary(monkeypatch, capsys):
    inputs = iter(["1", "Gas", "40", "other", "2023-07-15", "3", "2023", "7", "6"])
    _ = run_main_with_inputs(monkeypatch, inputs)
    captured = capsys.readouterr()
    assert "Category Summary" in captured.out
    assert "Other: $40.00" in captured.out


def test_main_view_summary_invalid_input(monkeypatch, capsys):
    inputs = iter(["3", "invalid-year", "6"])
    _ = run_main_with_inputs(monkeypatch, inputs)
    captured = capsys.readouterr()
    assert "Invalid input for year or month." in captured.out


def test_main_save_and_load(monkeypatch, tmp_path, capsys):
    filepath = tmp_path / "data.json"
    inputs = iter(
        [
            "1",
            "Rent",
            "1000",
            "housing",
            "2023-06-01",
            "4",
            str(filepath),
            "5",
            str(filepath),
            "6",
        ]
    )
    _ = run_main_with_inputs(monkeypatch, inputs)
    captured = capsys.readouterr()
    assert "Data saved" in captured.out
    assert "Data loaded" in captured.out


def test_main_save_load_errors(monkeypatch, capsys):
    inputs = iter(["4", "/", "5", "nonexistent.json", "6"])
    _ = run_main_with_inputs(monkeypatch, inputs)
    captured = capsys.readouterr()
    assert "Error saving file" in captured.out
    assert "Error loading file" in captured.out


def test_main_invalid_option(monkeypatch, capsys):
    inputs = iter(["10", "6"])
    _ = run_main_with_inputs(monkeypatch, inputs)
    captured = capsys.readouterr()
    assert "Invalid option" in captured.out
