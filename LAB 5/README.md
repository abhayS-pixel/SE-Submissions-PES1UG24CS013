# Lab 5: Static Code Analysis

Static analysis of `recruitment_tracker.py` (an SQLite-backed applicant tracking script for an HR team) using **Pylint**, **Bandit** and **Flake8**.

Source: https://github.com/SETAPESU26/L5_14_recruitment_tracker

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.47/10 | **10.00/10** |
| Bandit | 3 issues (2 Medium, 1 Low) | **No issues identified** |
| Flake8 | 8 issues | **0** |

The program's behaviour is unchanged. It still prints `['Nina']` and `2 in interview`, and it writes the same `applicants_report.csv`.

## Files

| File | Description |
|------|-------------|
| `recruitment_tracker.py` | Cleaned and fixed script |
| `issues.md` | Table of the 12 issues found, with line numbers, descriptions and fix approaches |
| `reflection.md` | Answers to the reflection questions |
| `pylint_report_before.txt` / `pylint_report_after.txt` | Pylint output before and after |
| `bandit_report_before.txt` / `bandit_report_after.txt` | Bandit output before and after |
| `flake8_report_before.txt` / `flake8_report_after.txt` | Flake8 output before and after |

## Key fixes

- **SQL injection (Bandit B608):** the INSERT now uses a parameterised query.
- **`eval()` (Bandit B307):** replaced with a safe `ast`-based parser that only allows numbers and `+ - * /`.
- **`except: pass` (Bandit B110):** now catches only `sqlite3.Error`, logs it, and returns a success flag.
- **Pylint:** snake_case names, docstrings, `with open` and the `csv` module, `shortlist` always returns a list, unused variable removed, `__main__` guard.
- **Flake8:** long lines wrapped, trailing whitespace removed, correct blank lines.

## Commits

1. Fix Bandit findings (plus the before reports)
2. Fix Pylint findings
3. Fix Flake8 findings
4. Add after reports, `issues.md` and `reflection.md`

## Reproduce

```bash
python3 -m venv venv && source venv/bin/activate
pip install pylint bandit flake8
python recruitment_tracker.py
pylint recruitment_tracker.py
bandit -r recruitment_tracker.py
flake8 recruitment_tracker.py
```
