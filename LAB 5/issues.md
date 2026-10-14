# Issues Found and Fixed — `recruitment_tracker.py`

Before: Pylint **4.47/10**, Bandit **3** issues (2 Medium, 1 Low), Flake8 **8** issues.
After: Pylint **10.00/10**, Bandit **0** issues, Flake8 **0** issues.

| # | Issue | Type | Line(s) (original) | Description | Fix Approach | Tool / Code |
|---|-------|------|---------|-------------|--------------|-------------|
| 1 | SQL injection in `addApplicant` | Security (Medium) | 8 | An f-string builds the INSERT, so a name like `x'); DROP TABLE applicants;--` is executed as SQL. | Use a parameterised query with `?` placeholders and pass the values as a tuple. Verified: the injection string is now stored as plain text. | Bandit B608 |
| 2 | `eval()` on user-supplied `salary_rule` | Security (Medium) | 14 | `eval` runs any Python expression, e.g. `__import__('os').system(...)`: arbitrary code execution. | Replaced with `parse_salary_rule()`, which parses with `ast` and evaluates only numbers and `+ - * /` (and unary +/-). Anything else raises `ValueError`. `2**9999999` is rejected too, which prevents a CPU-exhaustion attack. `ast.literal_eval` could not be used because it does not support `500000 + 150000`. | Bandit B307 / Pylint W0123 |
| 3 | Silent `except Exception: pass` | Bug / Security (Low) | 28-29 | Every database error was swallowed, so the caller never knew an update failed. Updating a non-existent ID also reported nothing. | Catch only `sqlite3.Error`, log it with `logging.exception`, and return `True`/`False` based on `cursor.rowcount`. | Bandit B110 / Pylint W0718 |
| 4 | Inconsistent return in `shortlist` | Bug | 20-21 | The function returned `None` when nobody qualified, so callers doing `for n in shortlist(...)` or `len(...)` would crash. | Return a list comprehension, so the result is always a list (empty if no match). | Pylint R1710 |
| 5 | Unused variable `total_seen` | Code quality | 15 | Dead code that was assigned but never used. | Removed. | Pylint W0612 / Flake8 F841 |
| 6 | File opened without `with`/encoding; manual CSV join | Resource leak / Bug | 32-35 | If a write failed, `f.close()` was never reached. No encoding was given. `",".join(row)` breaks on names containing commas and on `NULL` (None) values. | Use `with open(..., encoding="utf-8", newline="")` and `csv.writer` (quotes commas correctly, handles `None`). `lineterminator="\n"` keeps the original output format. | Pylint W1514, R1732 |
| 7 | camelCase function names | Style | 7, 24, 31, 38 | `addApplicant`, `updateStatus`, `exportReport`, `countByStatus` violate PEP 8. | Renamed to `add_applicant`, `update_status`, `export_report`, `count_by_status`. | Pylint C0103 |
| 8 | Missing docstrings | Documentation | module + every function | No documentation of purpose, parameters or return values. | Added a module docstring and a docstring to every function. | Pylint C0114, C0116 |
| 9 | Global DB connection and `main()` run at import | Design | 3, 52 | A module-level `conn` made functions depend on hidden global state, and importing the file ran the demo. | `create_connection()` returns the connection, which is passed explicitly to each function. Demo is guarded by `if __name__ == "__main__":`. | Design improvement (not flagged) |
| 10 | Lines too long | Style | 4, 8, 13, 26, 39 | Lines of 93-140 characters, over the 79 limit. | Wrapped SQL strings and calls over multiple lines. | Flake8 E501 / Pylint C0301 |
| 11 | Trailing whitespace | Style | 15 | Whitespace at end of line. | Removed. | Flake8 W291 / Pylint C0303 |
| 12 | Missing blank line before `exportReport` | Style | 31 | Only one blank line between top-level functions. | Two blank lines. | Flake8 E302 |

## Verification

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.47/10 (21 messages) | **10.00/10** |
| Bandit | 3 issues (2 Medium, 1 Low) | **No issues identified** |
| Flake8 | 8 issues | **0** |

The program output is unchanged: `['Nina']`, `2 in interview`, and an identical `applicants_report.csv`.
