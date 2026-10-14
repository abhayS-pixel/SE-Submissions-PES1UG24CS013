# Reflection

*(The handout PDF does not list the four questions, so these are the standard Lab 5 reflection questions.)*

**1. Which issues were the easiest and hardest to fix?**
Style issues (E501, W291, E302, snake_case, docstrings) were easy: they were mechanical, and Flake8 gave the exact line. The hardest was the `eval()`. Bandit suggests `ast.literal_eval`, but that does not accept `500000 + 150000`, so I had to write a small `ast`-based evaluator that allows only numbers and `+ - * /`. The silent `except: pass` was also tricky because the fix needed a design decision (log the error and return a success flag), not a one-line change.

**2. Did the tools report any false positives, or miss real problems?**
Nothing was a clear false positive. Bandit B608 would be a false positive for SQL built only from constants, but here it was a real injection. Several real problems were not flagged by any tool: the global database connection, `main()` running on import, and the fact that `shortlist` returned `None` was only caught as a style-looking message (R1710). The tools also say nothing about whether `parse_salary_rule` is a correct design. They complement human review rather than replace it.

**3. How would you integrate static analysis into your development workflow?**
Run Flake8 and Pylint in a pre-commit hook and in editor integration for instant feedback, then run all three tools plus the tests in CI (e.g. GitHub Actions) and fail the build on Bandit Medium/High findings or a Pylint score below a threshold (such as 9.5). Pinning tool versions and keeping a shared config file keeps results consistent across the team.

**4. What tangible improvements did you see in code quality, security and readability?**
Pylint went from 4.47 to 10.00, Bandit from 3 findings to 0, and Flake8 from 8 to 0. Security: SQL injection and arbitrary code execution through `eval` are closed (tested with a malicious name and a malicious rule). Reliability: database errors are logged instead of hidden, `shortlist` always returns a list, and the CSV export no longer leaks file handles or breaks on commas. Readability: consistent naming, docstrings, shorter lines and explicit dependencies make the file easier to read, test and reuse.
