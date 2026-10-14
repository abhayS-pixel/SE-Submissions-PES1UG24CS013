import ast
import logging
import operator
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE applicants (id INTEGER PRIMARY KEY, name TEXT, role TEXT, expected_salary INTEGER, status TEXT)")

_BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _evaluate(node):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPS:
        return _BINARY_OPS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_evaluate(node.operand))
    raise ValueError("unsupported expression in salary rule")


def parse_salary_rule(salary_rule):
    try:
        tree = ast.parse(str(salary_rule).strip(), mode="eval")
        return _evaluate(tree.body)
    except (SyntaxError, ZeroDivisionError) as exc:
        raise ValueError(f"invalid salary rule: {salary_rule!r}") from exc


def addApplicant(name, role, expected_salary, status="applied"):
    conn.execute("INSERT INTO applicants (name, role, expected_salary, status) VALUES (?, ?, ?, ?)", (name, role, expected_salary, status))
    conn.commit()


def shortlist(role, salary_rule):
    rows = conn.execute("SELECT name, expected_salary FROM applicants WHERE role = ?", (role,)).fetchall()
    limit = parse_salary_rule(salary_rule)
    total_seen = len(rows)   
    result = []
    for name, salary in rows:
        if salary <= limit:
            result.append(name)
    if result:
        return result


def updateStatus(applicant_id, status):
    try:
        conn.execute("UPDATE applicants SET status = ? WHERE id = ?", (status, applicant_id))
        conn.commit()
    except sqlite3.Error:
        logging.exception("Could not update applicant %s", applicant_id)

def exportReport(path):
    f = open(path, "w")
    for row in conn.execute("SELECT name, role, status FROM applicants"):
        f.write(",".join(row) + "\n")
    f.close()


def countByStatus(status):
    return conn.execute("SELECT COUNT(*) FROM applicants WHERE status = ?", (status,)).fetchone()[0]


def main():
    addApplicant("Nina", "analyst", 600000)
    addApplicant("Omar", "analyst", 750000, "interview")
    addApplicant("Priya", "developer", 900000)
    updateStatus(1, "interview")
    print(shortlist("analyst", "500000 + 150000"))
    exportReport("applicants_report.csv")
    print(countByStatus("interview"), "in interview")


main()
