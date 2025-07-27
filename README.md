## About the Personal Finance Tracker

A simple command-line application to help users manage their personal finances by tracking expenses. It enables users to add transactions, view summaries, and save or load their data from a file, making it easier to build good financial habits and maintain budgeting awareness.

### Features

- Add expense transactions  
- View finaexpensesncial summary
- Save/load transactions using JSON files  
- User-friendly CLI with input validation

### Requirements

- Python 3.7+
- uv

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/<yourusername>/finance-tracker.git
   cd finance-tracker
   ```

2. **Run the program**
   ```bash
   uv run python main.py
   ```

### Running Tests

Run:
```bash
uv run pytest
```

### Testing Highlights

- Uses `monkeypatch` to simulate user input  
- Captures console output using `capsys`


## Python Library Stack
A modern Python project setup using:
- [`tox`](https://tox.readthedocs.io/) – for test, lint, and format automation
- [`uv`](https://github.com/astral-sh/uv) – for fast dependency installation and environment management
- [`ruff`](https://docs.astral.sh/ruff/) – for linting and formatting
---

## 🧪 Run Tasks with Tox
### ✅ Run tests
```bash
uv run tox -e test
```

### 🔍 Run Ruff linter
```bash
uv run tox -e lint
```

### 🎨 Check formatting with Ruff
```bash
uv run tox -e format
```
---

## 💡 Manual Ruff Usage
If you want to run Ruff directly:

### Format the code
```bash
uv run ruff format .
```

### Check for lint issues
```bash
uv run ruff check .
```
---

## 📁 Project Structure
```
personal_finance_tracker/
├── tests/                  # Tests
├── requirements-test.txt   # Test dependencies
├── tox.ini                 # Tox environment definitions
├── pyproject.toml          # Tool configurations (ruff, etc)
└── README.md               # Project documentation
```
---

## ✅ Add More Tox Environments
You can expand the `tox.ini` file to include:
- Integration or end to end test suites
---

## 🧊 Using UV
This project uses [`uv`](https://github.com/astral-sh/uv) for:
- Creating fast virtual environments (`uv venv`)
- Installing packages (`uv pip install`)
- Installing dependencies in Tox (`installer = uv`)
---

## 🔗 Useful Links
- [Tox Documentation](https://tox.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [UV Project](https://github.com/astral-sh/uv)
---
