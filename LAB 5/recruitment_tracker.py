"""Applicant tracking for an HR team, backed by an SQLite database."""
import ast
import csv
import logging
import operator
import sqlite3

SCHEMA = "CREATE TABLE applicants (id INTEGER PRIMARY KEY, name TEXT, role TEXT, expected_salary INTEGER, status TEXT)"

_BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def create_connection(database=":memory:"):
    """Open a database connection and make sure the applicants table exists."""
    connection = sqlite3.connect(database)
    connection.execute(SCHEMA)
    return connection


def _evaluate(node):
    """Evaluate a parsed arithmetic expression made only of numbers and + - * /."""
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPS:
        return _BINARY_OPS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_evaluate(node.operand))
    raise ValueError("unsupported expression in salary rule")


def parse_salary_rule(salary_rule):
    """Safely turn a rule such as '500000 + 150000' into a number."""
    try:
        tree = ast.parse(str(salary_rule).strip(), mode="eval")
        return _evaluate(tree.body)
    except (SyntaxError, ZeroDivisionError) as exc:
        raise ValueError(f"invalid salary rule: {salary_rule!r}") from exc


def add_applicant(conn, name, role, expected_salary, status="applied"):
    """Insert a new applicant."""
    conn.execute("INSERT INTO applicants (name, role, expected_salary, status) VALUES (?, ?, ?, ?)", (name, role, expected_salary, status))
    conn.commit()


def shortlist(conn, role, salary_rule):
    """Return names of applicants for `role` whose salary is within the budget.

    An empty list is returned when nobody qualifies.
    """
    rows = conn.execute("SELECT name, expected_salary FROM applicants WHERE role = ?", (role,)).fetchall()
    limit = parse_salary_rule(salary_rule)
    return [name for name, salary in rows if salary <= limit]


def update_status(conn, applicant_id, status):
    """Update an applicant's status. Return True if a row was changed."""
    try:
        cursor = conn.execute("UPDATE applicants SET status = ? WHERE id = ?", (status, applicant_id))
        conn.commit()
    except sqlite3.Error:
        logging.exception("Could not update applicant %s", applicant_id)
        return False
    return cursor.rowcount > 0


def export_report(conn, path):
    """Write name, role and status of every applicant to a CSV file."""
    with open(path, "w", encoding="utf-8", newline="") as report:
        writer = csv.writer(report, lineterminator="\n")
        writer.writerows(conn.execute("SELECT name, role, status FROM applicants"))


def count_by_status(conn, status):
    """Return how many applicants currently have the given status."""
    return conn.execute("SELECT COUNT(*) FROM applicants WHERE status = ?", (status,)).fetchone()[0]


def main():
    """Run a short demonstration."""
    conn = create_connection()
    add_applicant(conn, "Nina", "analyst", 600000)
    add_applicant(conn, "Omar", "analyst", 750000, "interview")
    add_applicant(conn, "Priya", "developer", 900000)
    update_status(conn, 1, "interview")
    print(shortlist(conn, "analyst", "500000 + 150000"))
    export_report(conn, "applicants_report.csv")
    print(count_by_status(conn, "interview"), "in interview")
    conn.close()


if __name__ == "__main__":
    main()
